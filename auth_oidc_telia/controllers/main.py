# Copyright 2016 ICTSTUDIO <http://www.ictstudio.eu>
# Copyright 2021 ACSONE SA/NV <https://acsone.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import base64
import functools
import hashlib
import logging
import secrets
import json
import uuid
import requests
from time import time
from jwcrypto import jwk, jwt, jwe
from odoo import api, http, SUPERUSER_ID, _
from ast import literal_eval
from datetime import datetime, timedelta

from werkzeug.urls import url_decode, url_encode, url_unquote_plus, url_parse

from odoo.exceptions import AccessDenied
from odoo.addons.auth_oauth.controllers.main import OAuthLogin
from odoo.http import request, Response
from odoo.addons.web.controllers.utils import ensure_db, _get_login_redirect_url
from odoo.tools.misc import clean_context

_logger = logging.getLogger(__name__)

def fragment_to_query_string(func):
    @functools.wraps(func)
    def wrapper(self, *a, **kw):
        kw.pop('debug', False)
        if not kw:
            return Response("""<html><head><script>
                var l = window.location;
                var q = l.hash.substring(1);
                var r = l.pathname + l.search;
                if(q.length !== 0) {
                    var s = l.search ? (l.search === '?' ? '' : '&') : '?';
                    r = l.pathname + l.search + s + q;
                }
                if (r == l.pathname) {
                    r = '/';
                }
                window.location = r;
            </script></head><body></body></html>""")
        return func(self, *a, **kw)
    return wrapper

def find_jwk_by_use(jwks: jwk.JWKSet, use: str) -> jwk.JWK:
    if jwks is None:
        return None
    jwk = None
    for k in jwks:
        t = k.export(private_key=False, as_dict=True)
        if "use" in t and t["use"] == use:
            return k
        if not "use" in t:
            jwk = k
    return jwk

jwks_static_str = """
{
  "keys": [
    {
      "kty": "RSA",
      "use": "enc",
      "n": "xd2uDMtfXF55Adyf0MeRt6ZqCtoY02C0NugCkOhcKSbD_a5RhWBaPbasc5SjkZbuZRc4xc-Qu017W8FIpsn6pSrCc5x7Eo3QsD4FAAy6YSUBvqHb8zMaxLG41E6D0kMaeJU2HVt5HnT8rN2U66-1Z7VXwtrhW9KeBgxzv6plfWG3MkzrbAtV16E1sv64dFfoIJ_oMP71WKSrn_0KUjX6_1TThhKNxie6jcyQq0wsHDBM-6G4p8Mn_DL-zyq9PwkyTfC-ZHVKbLEqAbQUjBAbrbPt-hBNbw-LKtot6JYUHREOdS3pHrDtO1unVYOIsJr_XycKAxT49iCa6xemDQ4ndw",
      "e": "AQAB",
      "d": "SQpupCF099OWBtZrFnZ9N5aSYaQl8u2pSPV3cQedccFyKxSs2jf5x_tFiLsPcICPSzj5x6e6LTJKfdIJYCyCPnNc6bGTiwNXzJ9wWBbavF6dWMJGP-4XDRHwAUtkhPspa-bk3Yx1VwVneuanASPRKtH57h-_fhZvKBtzpQahRVlkDF_jwOs6aYHpKrML67ysgl0iZh3-lTuMPf-OeDVHPXK1tIY80_GR9LTzxLZZ5m8xm8MrxH3rLu45Y4ClzCw6XGxl6h99pnE576VI79um-38VVWTQJuNdLiF74R3H4kbykF3Z8wQjwb0lV6HuJ2TiwvOmQmey9UN-a1lkjtzW0Q",
      "p": "_nmf4R3kq6-moBI83MAovGOg8TevTWMcroM-sndr_KKX6cp7uSBo0H9XGSUlh3cuWSrDeqWft3EFbUzVVTJjuNx7KLWCUwDItgxD1aBP4-XpbSuaWcBz_kvavVNqEY8fr6LyYM-Al_lP5gITWZDzHqi_xPoKlS7ATmpcJVWaN-c",
      "q": "xw026238jmRwleLT5MOfQYEuTLMYyDcdov3xKvl2iRpf8JT-IbUZ3E1xUa_lFRwweYyN7m_VJfxndpo-J7K42BBhFDL2ln415af6NzHWob6zWMEwi6ERa43rG1RV6JjCXMqerjWcllDuJCQbt5lQcFSPTxZieVsA1VEGwvCnYfE",
      "dp": "9U-30SKpEtyEKyEJrOBNJLaCKqa8hkR6HL0GjrJS1jrDaSu5s0_L2to201Wc5Qb-FhUEVlIdMpBwY9pCeRvXSBi7XRYEqRFDa0NNjT06Zn53VLdI1yaQat8i4Yns4TpwmDbjonHGDDrZS-hKUPhLdg3EuBU2aHOmDLG5XIA155c",
      "dq": "fX4hT9Cp14QPTxAQkzuZ3gx5ijWnvCKzdp0vPO7GAq40KlNk3Q92XGQeu2dvwB1jml445UhwU2CMQkQAR7rvupio-7kdqcesZzu-DqpHLPYz0BMMbhuABhUVUsea2eflMec0n5SBQmuHmBWDu_7WrdtB9pSgRO5Q2iwZXTGn9aE",
      "qi": "RjP7419mfY5GfN_ni1o2LtPtKEYANMZbfW01ZbZDgob_Xmg1_X7FH0n1Tc9ez3hZQmUr1huswcnx2F8-QtFLzOIa9VGAWRMlVNAVG9EDh9ZqT4bZ8E5U3gXnTjmMryV9iCugfPjR29osQNmai6G6pmW70mqoOXgDr6cb80fBqaE",
      "kid": "J8w1gHx-9EgkzAnbvVyokxow-ESGvNC9CL3xpEIEE9A"
    },
    {
      "kty": "RSA",
      "use": "sig",
      "n": "qQE8yb5ecCvsBCshkWqeTVr-skqq9-vPOkrWcrwI29F6MFzy_WhfELU-rkTZKhbRqhnoPfgeQBG5ZbgKY32M9u6O1rUCmNXMiNhyh3j4j9WN5OzLJQbFzi3_rVClAcku_1GJKTl-1wVaeY7vFdF_C5nS49tQbIL0GOw6xDcWKF5PM1KG__odRys-szL7a1mOCxXA3I9THqTMJnJ0t_W6RIDBBj930RJarusw0oIVA7SVmHCInpLhoOiGAcE634PQlJJU1hgXGHRkKO6VAeZeXTiwQVonsE8Fe1veDLepHwTpJMfZd2vV4v83_sKem0RKdz9fyhKKVTGvaI1TtNwMvw",
      "e": "AQAB",
      "d": "H0SAV57l4ADwSJEmQ74jDZLBPoE8AmRZUaKY7F9HkEvAPIRl3GZb-D5gG2PXfcb9AWiLpDNsfVQKJfyXx3JqCyF1wdl5YodjsQnCnrfN3OaYuvroVrBbFltCS3F5Jcxv6oLOSpc9lVCDPawpJbM9uwq5jrh7t6e-u4GxGa5LZipHe8zJUSTaNq-RjbOtstaS4rMCTlIh9ujRXRfgSeXNoRDqPHtzi5Dr2v1jjA_ddplM6cve6SoqgyDavjAtQiwGpzKnE6bxMonKD_Yq6r4VcPRXoh_kCHBVpKV1bnuvipgbPu3BXMFQ5S6Cc7eUZ-HV5BmkEMvU7-ai-Kj5xYtLWQ",
      "p": "3v17M5iS78gNneLH5fUvBDsRSv9A--rqBM8QE054xVG7Wrva7bEhWjgwtdmfIVjee1jLrBNb4UjD7KJy8-CVkJxOhq4bnW9gFcu45_Q4_dZuj2e1bzr4V_6rUiwX_-a5AMkITNx7xemV55QHe7puS6Wjf17oJq7-PiKcjuOMaDs",
      "q": "wgXockCHmbD9fRA9PPmXYj2DhVABgMCaUlUu9hjwRGE0LNqPx3rd8tj2xNanKy-PZ2_p7fuUKRZC67FKckVb5T2jFZOPAWNtLkxQaHqfVTAU1hPnxfwun7NOz5F3kO7_izn3fl0wFerwrgzRYx3ZOwOzI93gehPJ22dtbzEZ6U0",
      "dp": "MckWQKbH55EauS1ww_7ByIgHjF8A-z2vkfNI-4aBoExnMBLRBlCNyb7R4Uf9J0zYH2Hr1zdbRCki1SpPz_NMcUT0o00sDTJYmYUqe18jekjt1kapU3QvDjZluarukMvKckpv9_kiCUXlmhaKtS0igvEwV7ewzTI0wVqo6Z4UMxE",
      "dq": "m0LXC_aPjHGRp-7C0nR4q-jFwnyPd1SpKZF5Dv5N5qpSckJEJEEyMw9kCYgsJebdPszTydk0atyhmLI6_M58ByoXw0Bdg6Loz8_J2JGnxye-xMERC-IN_UYjnv6tS5G1dNhiMQCpZiCnkOA4_rP4Db2cMOtwosALHEPb0srcDVE",
      "qi": "03ehSv_MkdxumfQMEEqhpHp88pTv_RWyG4woGdFB2DvcQe8wLOEzeC_3YAeyD7eKwSBHNMYsNTMp2sW4EXDOv1KO09t-1O-4RKzFW0Rz0VX1ngTyj_qVZwjx9MtK9WvFfId0PZ5BVdYrcEOrsr9uYbJ3Tov9lwybwJVolOJWJRw",
      "kid": "tAi2Jj4f1ngTgYaAVTQLoZvcOXGujOXgwc1n8CvOHzU"
    }
  ]
}
      """

jwks_static = jwk.JWKSet.from_json(jwks_static_str)

def get_provider_jwks(provider_id):
    provider = request.env['auth.oauth.provider'].with_user(SUPERUSER_ID).search([
        ('id', '=', int(provider_id))
    ])
    _logger.debug("JWKS STATIC STR: " + jwks_static_str)
    _logger.debug("JWKS JSON STR: " + str(provider.jwks_local))
    return jwks_static
    return jwk.JWKSet.from_json(provider.jwks_local)

def sign_request_object(provider_id, params):
    jwks = get_provider_jwks(provider_id)
    _logger.debug("HERE SIGN REQ JWKS: " + str(jwks))
    jwk = find_jwk_by_use(jwks, "sig")
    alg = "RS256"
    token = None
    token = jwt.JWT(
        header={"alg": alg, "typ": "JWT", "kid": jwk.kid},
        claims=params,
    )
    _logger.debug("HERE TOKEN: " + str(token))
    token.make_signed_token(jwk)
    return token

def sign_client_assertion(provider_id, claims):
    jwks = get_provider_jwks(provider_id)
    _logger.debug("HERE SIGN ASS JWKS: " + str(jwks))
    jwk = find_jwk_by_use(jwks, "sig")
    alg = "RS256"
    token = jwt.JWT(
        header={"alg": alg, "typ": "JWT"},
        claims=claims,
    )
    token.make_signed_token(jwk)
    return token


class OpenIDLogin(OAuthLogin):
    def list_providers(self):
        providers = super().list_providers()
        for provider in providers:
            flow = provider.get("flow")
            if flow in ("id_token", "id_token_code"):
                params = url_decode(provider["auth_link"].split("?")[-1])
                # nonce
                params["nonce"] = secrets.token_urlsafe()
                # response_type
                if flow == "id_token":
                    # https://openid.net/specs/openid-connect-core-1_0.html
                    # #ImplicitAuthRequest
                    params["response_type"] = "id_token token"
                elif flow == "id_token_code":
                    # https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest
                    params["response_type"] = "code"
                # PKCE (https://tools.ietf.org/html/rfc7636)
                code_verifier = provider["code_verifier"]
                code_challenge = base64.urlsafe_b64encode(
                    hashlib.sha256(code_verifier.encode("ascii")).digest()
                ).rstrip(b"=")
                params["code_challenge"] = code_challenge
                params["code_challenge_method"] = "S256"
                # scope
                if provider.get("scope"):
                    if "openid" not in provider["scope"].split():
                        _logger.error("openid connect scope must contain 'openid'")
                    params["scope"] = provider["scope"]

                # append provider specific auth link params
                if provider["auth_link_params"]:
                    params_upd = literal_eval(provider["auth_link_params"])
                    params.update(params_upd)

                # auth link that the user will click
                _logger.debug("HERE PROVIDER:" + str(provider))
                base_url = request.env["ir.config_parameter"].sudo().get_param("web.base.url")

                _logger.debug("HERE client_id: " + provider['client_id'])
                auth_request = dict()

                # Mandatory fields
                auth_request['iss'] = provider['client_id']
                auth_request['aud'] = provider['audience']
                auth_request['response_type'] = "code"
                auth_request['scope'] = provider['scope']
                auth_request['client_id'] = provider['client_id']
                # FIXME
                auth_request['redirect_uri'] = "http://localhost:8069/redirect"
                #auth_request['redirect_uri'] = str(str(base_url) + "/redirect")
                #_logger.debug("HERE redirect_uri: " + auth_request['redirect_uri'])

                # Optional fields
                auth_request['state'] = self.get_state(provider) # Not optional for Odoo
                auth_request['nonce'] = secrets.token_urlsafe()
                auth_request['jti'] = str(uuid.uuid4())

                # TODO
                #auth_request['ui_locales'] = Set to odoos language if fi/sv otherwise en
                auth_request_signed = sign_request_object(provider['id'], auth_request)
                params = dict(request=auth_request_signed)
                provider["auth_link"] = "{}?{}".format(
                    provider["auth_endpoint"], url_encode(params)
                )
        return providers

class OAuthController(http.Controller):

    #@http.route('/auth_oauth/signin', type='http', auth='none')
    @http.route('/redirect', type='http', auth='none')
    @fragment_to_query_string
    def signin(self, **kw):
        state = json.loads(kw['state'])
        _logger.debug("HERE SIGNIN STATE: " + str(state))

        # make sure request.session.db and state['d'] are the same,
        # update the session and retry the request otherwise
        dbname = state['d']
        if not http.db_filter([dbname]):
            return BadRequest()
        ensure_db(db=dbname)

        provider_id = state['p']
        provider = request.env['auth.oauth.provider'].with_user(SUPERUSER_ID).search([
            ('id', '=', int(provider_id))
        ])
        request.update_context(**clean_context(state.get('c', {})))
        try:
            # auth_oauth may create a new user, the commit makes it
            # visible to authenticate()'s own transaction below

            token_request = dict()

            # Mandatory fields
            token_request['iss'] = provider['client_id']
            token_request['sub'] = provider['client_id']
            token_request['aud'] = provider['token_audience']

            # Optional fields
            token_request['jti'] = str(uuid.uuid4())
            token_request['exp'] = int((datetime.now() + timedelta(minutes=10)).timestamp())

            _logger.debug("HERE TOKEN REQUEST JWT: " + str(token_request))
            jwt = sign_client_assertion(provider_id, token_request)
            _, login, key = request.env['res.users'].with_user(SUPERUSER_ID).auth_oauth(provider_id, kw, jwt)
            _logger.debug("HERE LOGIN: " + str(login))
            _logger.debug("HERE KEY: " + str(key))
            request.env.cr.commit()

            action = state.get('a')
            menu = state.get('m')
            redirect = url_unquote_plus(state['r']) if state.get('r') else False
            url = '/web'
            if redirect:
                url = redirect
            elif action:
                url = '/web#action=%s' % action
            elif menu:
                url = '/web#menu_id=%s' % menu

            pre_uid = request.session.authenticate(dbname, login, key)
            resp = request.redirect(_get_login_redirect_url(pre_uid, url), 303)
            resp.autocorrect_location_header = False

            # Since /web is hardcoded, verify user has right to land on it
            if url_parse(resp.location).path == '/web' and not request.env.user._is_internal():
                resp.location = '/'
            return resp
        #except AttributeError:  # TODO juc master: useless since ensure_db()
            # auth_signup is not installed
            #_logger.error("auth_signup not installed on database %s: oauth sign up cancelled.", dbname)
            #url = "/web/login?oauth_error=1"
        except AccessDenied:
            # oauth credentials not valid, user could be on a temporary session
            _logger.info('OAuth2: access denied, redirect to main page in case a valid session exists, without setting cookies')
            url = "/web/login?oauth_error=3"
        except Exception:
            # signup error
            _logger.exception("Exception during request handling")
            url = "/web/login?oauth_error=2"

        redirect = request.redirect(url, 303)
        redirect.autocorrect_location_header = False
        return redirect

    @http.route('/uas/oauth2/metadata.jwks', type='http', auth='none')
    def metadata_jwks(self, **kw):
        return "{}"

