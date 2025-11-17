# Copyright 2016 ICTSTUDIO <http://www.ictstudio.eu>
# Copyright 2021 ACSONE SA/NV <https://acsone.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import base64
import logging
import secrets
import json
import jwcrypto
import uuid

import requests

from odoo import api, fields, models, tools
from jwcrypto import jwk, jwt, jwe

_logger = logging.getLogger(__name__)

class AuthOauthProvider(models.Model):
    _inherit = "auth.oauth.provider"

    flow = fields.Selection(
        [
            ("access_token", "OAuth2"),
            ("id_token_code", "OpenID Connect (authorization code flow)"),
            ("id_token", "OpenID Connect (implicit flow, not recommended)"),
        ],
        string="Auth Flow",
        required=True,
        default="access_token",
    )
    audience = fields.Char(string="Audience")
    token_audience = fields.Char(string="Token Audience")
    token_map = fields.Char(
        help="Some Oauth providers don't map keys in their responses "
        "exactly as required.  It is important to ensure user_id and "
        "email at least are mapped. For OpenID Connect user_id is "
        "the sub key in the standard."
    )
    client_secret = fields.Char(
        help="Used in OpenID Connect authorization code flow for confidential clients.",
    )
    code_verifier = fields.Char(
        default=lambda self: secrets.token_urlsafe(32), help="Used for PKCE."
    )
    validation_endpoint = fields.Char(required=False)
    token_endpoint = fields.Char(
        string="Token URL", help="Required for OpenID Connect authorization code flow."
    )
    jwks_uri = fields.Char(string="Provider JWKS URL", help="Required for OpenID Connect.")
    jwks_local = fields.Text(string="Local JWKS", inverse="_compute_local_jwks", default="")
    jwks_public_local = fields.Text(string="Public keys of local JWKS", default="")
    use_jwks = fields.Boolean(string="Use JWKS")
    auth_link_params = fields.Char(
        help="Additional parameters for the auth link. "
        "For example: {'prompt':'select_account'}"
    )

    @api.onchange('jwks_local')
    def _compute_local_jwks(self):
        if not self.jwks_local or self.jwks_local.strip() == "":
            enc = jwcrypto.jwk.JWK.generate(kty='RSA', size=2048, kid=str(uuid.uuid4()))
            enc_dict = dict(enc)
            enc_dict['use'] = "enc"
            sig = jwcrypto.jwk.JWK.generate(kty='RSA', size=2048, kid=str(uuid.uuid4()))
            sig_dict = dict(sig)
            sig_dict['use'] = "sig"
            self.jwks_local = json.dumps(dict(keys=[enc_dict, sig_dict]), indent=2)
            self._compute_local_public_jwks()
        else:
            self.jwks_local = json.dumps(json.loads(self.jwks_local), indent=2)
            self._compute_local_public_jwks()

    def find_jwk_by_use(self, use):
        jwks = jwk.JWKSet.from_json(self.jwks_local)
        for k in jwks:
            t = k.export(private_key=False, as_dict=True)
            if t["use"] == use:
                return k

    def _compute_local_public_jwks(self):
        for provider in self:
            if not provider.jwks_local or provider.jwks_local == "":
                provider.jwks_public_local = ""
            else:
                try:
                    # Check that jwks_local is valid JSON and prettify it
                    provider.jwks_local = json.dumps(json.loads(provider.jwks_local), indent=2)
                    enc = provider.find_jwk_by_use("enc")
                    enc_dict = enc.export(private_key=False, as_dict=True)
                    enc_dict['use'] = "enc"
                    enc_dict['alg'] = "RSA256"
                    sig = provider.find_jwk_by_use("sig")
                    sig_dict = sig.export(private_key=False, as_dict=True)
                    sig_dict['use'] = "sig"
                    sig_dict['alg'] = "RSA256"
                    provider.jwks_public_local = json.dumps(dict(keys=[enc_dict, sig_dict]), indent=2)
                except:
                    provider.jwks_public_local = ""

    def _telia_get_keys(self):
        r = requests.get(self.jwks_uri, timeout=10)
        r.raise_for_status()
        response = r.json()
        return response["keys"]

    def _telia_map_token_values(self, res):
        if self.token_map:
            for pair in self.token_map.split(" "):
                from_key, to_key = (k.strip() for k in pair.split("=", 1))
                if to_key not in res:
                    res[to_key] = res.get(from_key, "")
        return res

    def _telia_parse_id_token(self, id_token, access_token):
        self.ensure_one()
        res = {}
        res.update(self._telia_decode_id_token(access_token, id_token))
        res.update(self._telia_map_token_values(res))
        return res

    def _telia_decode_id_token(self, access_token, id_token):
        jwks = jwk.JWKSet.from_json(json.dumps(dict(keys=self._telia_get_keys())))
        local_jwks = jwk.JWKSet.from_json(self.jwks_local)
        token = jwe.JWE()
        token.deserialize(id_token, key=local_jwks)
        id_jwt = jwt.JWT()
        id_jwt.deserialize(token.payload.decode('utf-8'), key=jwks)
        return json.loads(str(id_jwt.claims))
