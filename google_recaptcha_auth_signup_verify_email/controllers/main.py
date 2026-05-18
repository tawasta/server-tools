import logging

from odoo import _
from odoo.http import request

from odoo.addons.auth_signup_verify_email.controllers.main import SignupVerifyEmail

_logger = logging.getLogger(__name__)


class SignupVerifyEmailRecaptcha(SignupVerifyEmail):
    def passwordless_signup(self):
        """Enforce recaptcha before triggering the signup-confirmation email,
        to avoid sending emails due to bots."""
        if not request.env["ir.http"]._verify_request_recaptcha_token("signup"):
            qcontext = self.get_auth_signup_qcontext()
            qcontext["error"] = _("Suspicious activity detected by Google reCaptcha.")
            return request.render("auth_signup.signup", qcontext)
        return super().passwordless_signup()
