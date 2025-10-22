# Copyright 2016 ICTSTUDIO <http://www.ictstudio.eu>
# Copyright 2021 ACSONE SA/NV <https://acsone.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import base64
import logging
import secrets
import json

import requests

from odoo import api, fields, models, tools
from jwcrypto import jwk, jwt, jwe

_logger = logging.getLogger(__name__)

from jose import jwt as jose_jwt
from jose.exceptions import JWSError, JWTError


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
    jwks_local = fields.Text(
            string="Local JWKS",
            inverse="_compute_jwks",
            default=""
    )
    auth_link_params = fields.Char(
        help="Additional parameters for the auth link. "
        "For example: {'prompt':'select_account'}"
    )

    @api.depends("jwks_local")
    def _compute_jwks(self):
        if not self.jwks_local or self.jwks_local == "":
            sig = jwk.JWK.generate(kty='RSA', size=2048, kid="1234567890")
            enc = jwk.JWK.generate(kty='RSA', size=2048, kid="0987654321")
            self.jwks_local = json.dumps(dict(keys=[sig, enc]))
        _logger.debug("HERE JWKS_LOCAL: " + str(self.jwks_local))

    @tools.ormcache("self.jwks_uri", "kid")
    def _get_keys(self, kid):
        r = requests.get(self.jwks_uri, timeout=10)
        r.raise_for_status()
        response = r.json()
        # the keys returned here should follow
        # JWS Notes on Key Selection
        # https://datatracker.ietf.org/doc/html/draft-ietf-jose-json-web-signature#appendix-D
        return [
            key
            for key in response["keys"]
            if kid is None or key.get("kid", None) == kid
        ]

    def _map_token_values(self, res):
        if self.token_map:
            for pair in self.token_map.split(" "):
                _logger.debug("HERE PAIR:" + str(pair))
                from_key, to_key = (k.strip() for k in pair.split(":", 1))
                if to_key not in res:
                    res[to_key] = res.get(from_key, "")
        return res

    def _parse_id_token(self, id_token, access_token):
        self.ensure_one()
        res = {}
        res.update(self._decode_id_token(access_token, id_token))
        res.update(self._map_token_values(res))
        _logger.debug("HERE RES:" + str(res))
        return res

    def _decode_id_token(self, access_token, id_token):
        local_jwks = jwk.JWKSet.from_json(self.jwks_local)
        token = jwe.JWE()
        token.deserialize(id_token, key=local_jwks)
        #jwetoken.decrypt(local_jwks)
        payload = base64.urlsafe_b64decode(token.payload)
        _logger.debug("HERE PAYLOAD:" + payload)
        return json.loads(str(token))
