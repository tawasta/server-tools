from odoo import http
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
import logging

_logger = logging.getLogger(__name__)


class AuthSignupPortalUserCustomRedirectHome(AuthSignupHome):
    def get_auth_signup_qcontext(self):
        """
        Fetch partner_firstname module's name order config
        """

        qcontext = super(
            AuthSignupPortalUserCustomRedirectHome, self
        ).get_auth_signup_qcontext()

        default_order = request.env["res.partner"]._names_order_default()

        qcontext["partner_names_order"] = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_names_order", default_order)
        )

        return qcontext
