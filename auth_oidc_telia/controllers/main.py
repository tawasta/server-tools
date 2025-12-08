# Copyright 2016 ICTSTUDIO <http://www.ictstudio.eu>
# Copyright 2021 ACSONE SA/NV <https://acsone.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import base64
import functools
import hashlib
import json
import logging
import secrets
import uuid
from ast import literal_eval
from datetime import timedelta

from jwcrypto import jwt
from werkzeug.exceptions import BadRequest
from werkzeug.urls import url_decode, url_encode, url_parse, url_unquote_plus

from odoo import SUPERUSER_ID, fields, http
from odoo.exceptions import AccessDenied
from odoo.http import Response, request
from odoo.tools.misc import clean_context

from odoo.addons.auth_oauth.controllers.main import OAuthLogin
from odoo.addons.web.controllers.utils import _get_login_redirect_url, ensure_db

_logger = logging.getLogger(__name__)


def fragment_to_query_string(func):
    @functools.wraps(func)
    def wrapper(self, *a, **kw):
        kw.pop("debug", False)
        if not kw:
            return Response(
                """<html><head><script>
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
                </script></head><body></body></html>"""
            )
        return func(self, *a, **kw)

    return wrapper


def sign_request_object(provider_id, params):
    provider = (
        request.env["auth.oauth.provider"]
        .with_user(SUPERUSER_ID)
        .search([("id", "=", int(provider_id))])
    )
    jwk = provider.find_jwk_by_use("sig")
    alg = "RS256"
    token = None
    token = jwt.JWT(
        header={"alg": alg, "typ": "JWT", "kid": jwk.kid},
        claims=params,
    )
    token.make_signed_token(jwk)
    return token


def sign_client_assertion(provider_id, claims):
    provider = (
        request.env["auth.oauth.provider"]
        .with_user(SUPERUSER_ID)
        .search([("id", "=", int(provider_id))])
    )
    jwk = provider.find_jwk_by_use("sig")
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
            if provider["use_jwks"]:
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
                    base_url = (
                        request.env["ir.config_parameter"]
                        .sudo()
                        .get_param("web.base.url")
                    )

                    auth_request = dict()

                    # Mandatory fields
                    auth_request["iss"] = provider["client_id"]
                    auth_request["aud"] = provider["audience"]
                    auth_request["response_type"] = "code"
                    auth_request["scope"] = provider["scope"]
                    auth_request["client_id"] = provider["client_id"]
                    auth_request["redirect_uri"] = "http://localhost:8069/redirect"
                    if str(base_url) != "http://localhost:8069":
                        auth_request["redirect_uri"] = str(
                            str(base_url) + "/signin_telia"
                        )

                    # Optional fields
                    auth_request["state"] = self.get_state(
                        provider
                    )  # Not optional for Odoo
                    auth_request["nonce"] = secrets.token_urlsafe()
                    auth_request["jti"] = str(uuid.uuid4())

                    # TODO
                    # auth_request["ui_locales"] = Set to odoos language
                    # if fi/sv otherwise en
                    auth_request_signed = sign_request_object(
                        provider["id"], auth_request
                    )
                    params = dict(request=auth_request_signed)
                    provider["auth_link"] = "{}?{}".format(
                        provider["auth_endpoint"], url_encode(params)
                    )
            else:
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
                    provider["auth_link"] = "{}?{}".format(
                        provider["auth_endpoint"], url_encode(params)
                    )
        return providers


class OAuthController(http.Controller):
    # /redirect is for local testing
    @http.route(
        ["/redirect", "/signin_telia", "/signing_telia"], type="http", auth="none"
    )
    @fragment_to_query_string
    def telia_signin(self, **kw):
        state = json.loads(kw["state"])

        # make sure request.session.db and state["d"] are the same,
        # update the session and retry the request otherwise
        dbname = state["d"]
        if not http.db_filter([dbname]):
            return BadRequest()
        ensure_db(db=dbname)

        provider_id = state["p"]
        provider = (
            request.env["auth.oauth.provider"]
            .with_user(SUPERUSER_ID)
            .search([("id", "=", int(provider_id))])
        )
        request.update_context(**clean_context(state.get("c", {})))
        try:
            # auth_oauth may create a new user, the commit makes it
            # visible to authenticate()'s own transaction below

            token_request = dict()

            # Mandatory fields
            token_request["iss"] = provider["client_id"]
            token_request["sub"] = provider["client_id"]
            token_request["aud"] = provider["token_audience"]

            # Optional fields
            token_request["jti"] = str(uuid.uuid4())
            token_request["exp"] = int(
                (fields.datetime.now() + timedelta(minutes=10)).timestamp()
            )

            jwt = sign_client_assertion(provider_id, token_request)
            _, login, key = (
                request.env["res.users"]
                .with_user(SUPERUSER_ID)
                .auth_oauth(provider_id, kw, jwt)
            )
            request.env.cr.commit()

            action = state.get("a")
            menu = state.get("m")
            redirect = url_unquote_plus(state["r"]) if state.get("r") else False
            url = "/web"
            if redirect:
                url = redirect
            elif action:
                url = "/web#action=%s" % action
            elif menu:
                url = "/web#menu_id=%s" % menu

            pre_uid = request.session.authenticate(dbname, login, key)
            resp = request.redirect(_get_login_redirect_url(pre_uid, url), 303)
            resp.autocorrect_location_header = False

            # Since /web is hardcoded, verify user has right to land on it
            if (
                url_parse(resp.location).path == "/web"
                and not request.env.user._is_internal()
            ):
                resp.location = "/"
            return resp
        # except AttributeError:  # TODO juc master: useless since ensure_db()
        # auth_signup is not installed
        # _logger.error("auth_signup not installed on database %s:
        # oauth sign up cancelled.", dbname)
        # url = "/web/login?oauth_error=1"
        except AccessDenied:
            # oauth credentials not valid, user could be on a temporary session
            _logger.info(
                """OAuth2: access denied, redirect to main page in case a
                valid session exists, without setting cookies"""
            )
            url = "/web/login?oauth_error=3"
        except Exception:
            # signup error
            _logger.exception("Exception during request handling")
            url = "/web/login?oauth_error=2"

        redirect = request.redirect(url, 303)
        redirect.autocorrect_location_header = False
        return redirect

    @http.route(
        [
            "/uas/oauth2/metadata.jwks",
            "/<string:provider_name>/openid_relying_party/signed_jwks.jwt",
        ],
        type="http",
        auth="none",
    )
    def openid_relying_party_signed_jwks(self, **kw):
        provider_name = kw.pop("provider_name", False)
        provider = (
            request.env["auth.oauth.provider"]
            .with_user(SUPERUSER_ID)
            .search([("name", "=", provider_name)])
        )
        jwk = provider.find_jwk_by_use("sig")
        alg = "RS256"
        signed_jwks = None
        signed_jwks = jwt.JWT(
            header={"alg": alg, "typ": "JWT", "kid": jwk.kid},
            claims=provider["jwks_public_local"],
        )
        signed_jwks.make_signed_token(jwk)
        return str(signed_jwks.serialize())
