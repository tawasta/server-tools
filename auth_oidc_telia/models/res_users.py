# Copyright 2016 ICTSTUDIO <http://www.ictstudio.eu>
# Copyright 2021 ACSONE SA/NV <https://acsone.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

import requests

from odoo import api, models
from odoo.exceptions import AccessDenied
from odoo.http import request
from jwcrypto import jwk, jwt, jwe

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = "res.users"


    def _auth_oauth_get_tokens_auth_code_flow(self, oauth_provider, params, jwt):
        # https://openid.net/specs/openid-connect-core-1_0.html#AuthResponse
        code = params.get("code")
        # https://openid.net/specs/openid-connect-core-1_0.html#TokenRequest
        auth = None
        if oauth_provider.client_secret:
            auth = (oauth_provider.client_id, oauth_provider.client_secret)
        if oauth_provider.use_jwks:
            request_data=dict(
                grant_type="authorization_code",
                redirect_uri=request.httprequest.url_root + "redirect",
                code=code,
                client_id=oauth_provider.client_id,
                client_assertion_type = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                client_assertion = jwt.serialize(),
            )
            req = requests.Request("POST", oauth_provider.token_endpoint, data=request_data)
            prepared = req.prepare()
            #response = requests.post( oauth_provider.token_endpoint, data=request_data, auth=auth, timeout=10,)
            s = requests.Session()
            response = s.send(prepared)
        else:
            response = requests.post(
                oauth_provider.token_endpoint,
                data=dict(
                    client_id=oauth_provider.client_id,
                    grant_type="authorization_code",
                    code=code,
                    code_verifier=oauth_provider.code_verifier,  # PKCE
                    redirect_uri=request.httprequest.url_root + "auth_oauth/signin",
                ),
                auth=auth,
                timeout=10,
            )
        response.raise_for_status()
        response_json = response.json()
        # https://openid.net/specs/openid-connect-core-1_0.html#TokenResponse
        return response_json.get("access_token"), response_json.get("id_token")

    @api.model
    def _generate_signup_values(self, provider, validation, params):
        oauth_uid = validation['user_id']
        email = validation.get('email', 'provider_%s_user_%s' % (provider, oauth_uid))
        firstname = validation.get('firstname', "")
        lastname = validation.get('lastname', "")
        if firstname != "" and lastname != "":
            name = firstname + " " + lastname
        else:
            name = validation.get('name', email)
        return {
            'firstname': firstname,
            'lastname': lastname,
            'name': name,
            'login': email,
            'email': email,
            'oauth_provider_id': provider,
            'oauth_uid': oauth_uid,
            'oauth_access_token': params['access_token'],
            'active': True,
        }

    @api.model
    def auth_oauth(self, provider, params, token_fetch_jwt=""):
        oauth_provider = self.env["auth.oauth.provider"].browse(provider)
        if oauth_provider.flow == "id_token":
            access_token, id_token = self._auth_oauth_get_tokens_implicit_flow(
                oauth_provider, params
            )
        elif oauth_provider.flow == "id_token_code":
            access_token, id_token = self._auth_oauth_get_tokens_auth_code_flow(
                oauth_provider, params, token_fetch_jwt
            )
        else:
            return super().auth_oauth(provider, params)
        if not access_token:
            _logger.error("No access_token in response.")
            raise AccessDenied()
        if not id_token:
            _logger.error("No id_token in response.")
            raise AccessDenied()
        validation = oauth_provider._telia_parse_id_token(id_token, access_token)
        # required check
        if "user_id" not in validation:
            _logger.error("user_id claim not found in id_token (after mapping).")
            raise AccessDenied()
        # retrieve and sign in user
        params["access_token"] = access_token
        login = self._auth_oauth_signin(provider, validation, params)
        if not login:
            raise AccessDenied()
        # return user credentials
        return (self.env.cr.dbname, login, access_token)
