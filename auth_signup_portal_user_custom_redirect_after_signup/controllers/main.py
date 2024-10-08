from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
import logging

_logger = logging.getLogger(__name__)


class AuthSignupPortalUserCustomRedirectHome(AuthSignupHome):
    def get_auth_signup_qcontext(self):
        # Extract the origin URL, and place it into qcontext where it will be
        # passed to res.users record creation

        qcontext = super(
            AuthSignupPortalUserCustomRedirectHome, self
        ).get_auth_signup_qcontext()

        base_url = request.env["ir.config_parameter"].sudo().get_param("web.base.url")
        portal_user_signup_origin_url = request.params.get(
            "portal_user_signup_origin_url"
        )

        # Don't allow pointing outside the installation base address
        if (
            portal_user_signup_origin_url
            and base_url
            and portal_user_signup_origin_url.startswith(base_url)
        ):
            qcontext["portal_user_signup_origin_url"] = portal_user_signup_origin_url
        else:
            _logger.info(
                "URL %s does not match base url %s, skipping"
                % (portal_user_signup_origin_url, base_url)
            )

        return qcontext
