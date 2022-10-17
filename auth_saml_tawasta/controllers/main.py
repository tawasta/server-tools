# Copyright (C) 2020 GlodoUK <https://www.glodo.uk/>
# Copyright (C) 2010-2016, 2022 XCG Consulting <https://xcg-consulting.fr/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import functools
import json
import logging
import re

import saml2.xmldsig as ds
import werkzeug.utils
from saml2 import BINDING_HTTP_REDIRECT
from saml2.ident import code, decode
from saml2.response import StatusError
from saml2.time_util import in_a_while
from werkzeug.urls import url_quote_plus

import odoo
from odoo import SUPERUSER_ID, _, api, http, models, registry as registry_get
from odoo.http import request

from odoo.addons.web.controllers.main import (
    Home,
    Session,
    ensure_db,
    login_and_redirect,
    set_cookie_and_redirect,
)

_logger = logging.getLogger(__name__)


# ----------------------------------------------------------
# helpers
# ----------------------------------------------------------


def fragment_to_query_string(func):
    @functools.wraps(func)
    def wrapper(self, req, **kw):
        if not kw:
            return """<html><head><script>
                var l = window.location;
                var q = l.hash.substring(1);
                var r = '/' + l.search;
                if(q.length !== 0) {
                    var s = l.search ? (l.search === '?' ? '' : '&') : '?';
                    r = l.pathname + l.search + s + q;
                }
                window.location = r;
            </script></head><body></body></html>"""
        return func(self, req, **kw)

    return wrapper


# ----------------------------------------------------------
# Controller
# ----------------------------------------------------------


class SAMLLogin(Home):
    def _list_saml_providers_domain(self):
        return []

    def list_saml_providers(self, with_autoredirect: bool = False) -> models.Model:
        """Return available providers

        :param with_autoredirect: True to only list providers with automatic redirection
        :return: a recordset of providers
        """
        domain = self._list_saml_providers_domain()
        if with_autoredirect:
            domain.append(("autoredirect", "=", True))
        providers = request.env["auth.saml.provider"].sudo().search_read(domain)

        for provider in providers:
            # Compatibility with auth_oauth/controllers/main.py in order to
            # avoid KeyError rendering template_auth_oauth_providers
            provider.setdefault("auth_link", "")
        return providers

    def _saml_autoredirect(self):
        # automatically redirect if any provider is set up to do that
        autoredirect_providers = self.list_saml_providers(True)
        # do not redirect if asked too or if a SAML error has been found
        disable_autoredirect = (
            "disable_autoredirect" in request.params or "error" in request.params
        )
        if autoredirect_providers and not disable_autoredirect:
            return werkzeug.utils.redirect(
                "/auth_saml/get_auth_request?pid=%d" % autoredirect_providers[0]["id"],
                303,
            )
        return None

    @http.route()
    def web_client(self, s_action=None, **kw):
        ensure_db()
        if not request.session.uid:
            result = self._saml_autoredirect()
            if result:
                return result
        return super().web_client(s_action, **kw)

    @http.route()
    def web_login(self, redirect=None, *args, **kw):
        ensure_db()
        if (
            request.httprequest.method == "GET"
            and request.session.uid
            and request.params.get("redirect")
        ):

            # Redirect if already logged in and redirect param is present
            return http.redirect_with_hash(request.params.get("redirect"))

        if request.httprequest.method == "GET":
            result = self._saml_autoredirect()
            if result:
                return result

        providers = self.list_saml_providers()

        response = super().web_login(redirect, *args, **kw)
        if response.is_qweb:
            error = request.params.get("saml_error")
            if error == "no-signup":
                error = _("Sign up is not allowed on this database.")
            elif error == "access-denied":
                error = _("Access Denied")
            elif error == "expired":
                error = _(
                    "You do not have access to this database. Please contact"
                    " support."
                )
            else:
                error = None

            response.qcontext["providers"] = providers

            if error:
                response.qcontext["error"] = error

        return response


class AuthSAMLController(http.Controller):
    def _get_saml_extra_relaystate(self):
        """
        Compute any additional extra state to be sent to the IDP so it can
        forward it back to us. This is called RelayState.

        The provider will automatically set things like the dbname, provider
        id, etc.
        """

        redirect = request.params.get("redirect") or "/"
        if not redirect.startswith(("//", "http://", "https://")):
            redirect = "{}{}".format(
                request.httprequest.url_root,
                redirect[1:] if redirect[0] == "/" else redirect,
            )

        state = {
            "r": url_quote_plus(redirect),
        }
        return state

    @http.route("/auth_saml/get_auth_request", type="http", auth="none")
    def get_auth_request(self, pid, redirect=None):
        provider_id = int(pid)

        provider = request.env["auth.saml.provider"].sudo().browse(provider_id)
        redirect_url = provider._get_auth_request(
            self._get_saml_extra_relaystate(), request.httprequest.url_root.rstrip("/")
        )
        if not redirect_url:
            raise Exception(
                "Failed to get auth request from provider. "
                "Either misconfigured SAML provider or unknown provider."
            )

        redirect = werkzeug.utils.redirect(redirect_url, 303)
        redirect.autocorrect_location_header = True
        return redirect

    @http.route("/auth_saml/signin", type="http", auth="none", csrf=False)
    @fragment_to_query_string
    # pylint: disable=unused-argument
    def signin(self, req, **kw):
        """
        Client obtained a saml token and passed it back
        to us... we need to validate it
        """
        saml_response = kw.get("SAMLResponse")

        if kw.get("RelayState") is None:
            # here we are in front of a client that went through
            # some routes that "lost" its relaystate... this can happen
            # if the client visited his IDP and successfully logged in
            # then the IDP gave him a portal with his available applications
            # but the provided link does not include the necessary relaystate
            url = "/?type=signup"
            redirect = werkzeug.utils.redirect(url, 303)
            redirect.autocorrect_location_header = True
            return redirect

        state = json.loads(kw["RelayState"])
        provider = state["p"]
        dbname = state["d"]
        context = state.get("c", {})
        registry = registry_get(dbname)

        with registry.cursor() as cr:
            try:
                env = api.Environment(cr, SUPERUSER_ID, context)
                credentials = (
                    env["res.users"]
                    .sudo()
                    .auth_saml(
                        provider,
                        saml_response,
                        request.httprequest.url_root.rstrip("/"),
                    )
                )
                action = state.get("a")
                menu = state.get("m")
                redirect = (
                    werkzeug.url_unquote_plus(state["r"]) if state.get("r") else False
                )
                if redirect:
                    url = redirect
                elif action:
                    url = "/#action=%s" % action
                elif menu:
                    url = "/#menu_id=%s" % menu
                return login_and_redirect(*credentials, redirect_url=url)

            except odoo.exceptions.AccessDenied:
                # saml credentials not valid,
                # user could be on a temporary session
                _logger.info("SAML2: access denied")

                url = "/web/login?saml_error=expired"
                redirect = werkzeug.utils.redirect(url, 303)
                redirect.autocorrect_location_header = False
                return redirect

            except Exception as e:
                # signup error
                _logger.exception("SAML2: failure - %s", str(e))
                url = "/web/login?saml_error=access-denied"

        return set_cookie_and_redirect(url)

    @http.route("/auth_saml/metadata", type="http", auth="none", csrf=False)
    # pylint: disable=unused-argument
    def saml_metadata(self, req, **kw):
        provider = kw.get("p")
        dbname = kw.get("d")
        valid = kw.get("valid", None)

        if not dbname or not provider:
            _logger.debug("Metadata page asked without database name or provider id")
            return request.not_found(_("Missing parameters"))

        provider = int(provider)

        registry = registry_get(dbname)

        with registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            client = env["auth.saml.provider"].sudo().browse(provider)
            if not client.exists():
                return request.not_found(_("Unknown provider"))

            return request.make_response(
                client._metadata_string(
                    valid, request.httprequest.url_root.rstrip("/")
                ),
                [("Content-Type", "text/xml")],
            )

    @http.route("/auth_saml/slo", type="http", auth="none", csrf=False)
    @fragment_to_query_string
    def slo_request(self, req, *args, **kwargs):
        """
        This method is called from IdP in two different cases:
        1. We sent a logout request to IdP and IdP responses to this method (LogoutResponse)
        2. IdP sends logout request to us and we respond to IdP (LogoutRequest handling)
        :param req: request calling this method
        :param args: args
        :param kwargs: kwargs
        :return: redirect
        """
        provider = request.env["auth.saml.provider"].sudo().search([], limit=1)
        client = provider._get_client_for_provider(
            request.httprequest.url_root.rstrip("/")
        )
        # LogoutResponse handling STARTS
        if "SAMLResponse" in kwargs:
            _logger.warning("LogoutResponse handling started")
            try:
                response = client.parse_logout_request_response(
                    kwargs.get("SAMLResponse"), BINDING_HTTP_REDIRECT
                )
            except StatusError as e:
                response = None
                _logger.warning("Error logging out from remote provider: " + str(e))
            if response and response.status_ok():
                # Successfull LogoutResponse handling
                return werkzeug.utils.redirect("/", 303)
        # LogoutResponse handling ENDS
        # LogoutRequest handling STARTS
        elif "SAMLRequest" in kwargs:
            # How do we figure out the NameID
            _logger.warning("LogoutRequest handling started")
            # TODO: This is ugly workaround to get the NameID
            # most likely the correct procedure is to get the NameID Odoo
            # details (cache, session, ...). Now we get it from the requests
            # so it's always true.
            xmlreq = client.parse_logout_request(
                xmlstr=kwargs.get("SAMLRequest"),
                binding=BINDING_HTTP_REDIRECT,
                relay_state=kwargs.get("RelayState", ""),
            )
            name_id = xmlreq.message.name_id
            saml_token = (
                request.env["res.users.saml"]
                .sudo()
                .search(
                    [
                        ("saml_name_id", "=", code(name_id)),
                    ]
                )
            )
            if not saml_token:
                # No SAML token, skip
                _logger.warning("SAML token not found, aborting...")
                return werkzeug.utils.redirect("/", 303)
            http_info = client.handle_logout_request(
                request=kwargs.get("SAMLRequest"),
                name_id=name_id,
                binding=BINDING_HTTP_REDIRECT,
                relay_state=kwargs.get("RelayState", ""),
            )
            # Destroy user sessions in Odoo
            target_uid = saml_token.user_id.id
            sessions = http.root.session_store.list()
            for sess in sessions:
                session_store = http.root.session_store
                session = session_store.get(sess)
                if session.sid and session.uid == target_uid:
                    session_store.delete(session)
            return werkzeug.utils.redirect(http_info.get("headers")[0][1], 303)
        # LogoutRequest handling ENDS
        # If we end up here, then request wasn't LogoutRequest or LogoutResponse
        # --> Error?
        _logger.warning("Request wasn't LogoutRequest or LogoutResponse, error?")
        return werkzeug.utils.redirect("/", 303)


class SAMLSession(Session):
    @http.route()
    def logout(self, redirect="/web"):
        """Logout user from IDP as well"""
        saml_token = (
            request.env["res.users.token"]
            .sudo()
            .search(
                [
                    ("user_id", "=", request.session.uid),
                ]
            )
        )
        if request.session.get("_saml_user") and saml_token:
            _logger.warning("Initiating SAML SLO-sequence...")
            # Here we create LogoutRequest and send it to IdP
            provider = request.env["auth.saml.provider"].sudo().search([], limit=1)
            name_id = decode(saml_token.saml_name_id)
            client = provider._get_client_for_provider(
                request.httprequest.url_root.rstrip("/")
            )
            sig_alg = ds.SIG_RSA_SHA256
            service_location = re.search(
                r"SingleLogoutService\sBinding=\".*HTTP-Redirect\"\sLocation=\"(.*)\"",
                provider.idp_metadata,
            ).group(1)
            idp_entity_id = re.search(
                r"\sentityID=\"(.*)\"", provider.idp_metadata
            ).group(0)
            if not (service_location and idp_entity_id):
                _logger.error(
                    "Tried to SLO but didn't find IDP service and IDP entity ID"
                )
                return super().logout(redirect)
            req_id, req = client.create_logout_request(
                service_location,
                idp_entity_id,
                name_id=name_id,
                reason="User logout",
                expire=in_a_while(minutes=5),
                sign_alg=sig_alg,
            )
            relay_state = {
                "d": request.env.cr.dbname,
                "p": provider.id,
            }
            # relay_state = client._relay_state(req_id)
            binding = BINDING_HTTP_REDIRECT
            http_info = client.apply_binding(
                binding,
                str(req),
                service_location,
                relay_state,
                sign=provider.sign,
                sigalg=sig_alg,
            )
            results = {}
            results[idp_entity_id] = (binding, http_info)
            redirect = http_info.get("headers")[0][1]
            # TODO: Should the auth_saml_token be deleted?
        return super().logout(redirect)
