import logging

from odoo import _
from odoo.exceptions import UserError
from odoo.http import request

from odoo.addons.auth_signup_verify_email.controllers.main import SignupVerifyEmail

_logger = logging.getLogger(__name__)


class SignupVerifyEmailRecaptcha(SignupVerifyEmail):
    def passwordless_signup(self):
        """Enforce recaptcha also when confirming user accounts via an email link,
        to avoid mass sending useless emails due to bot triggers"""

        if not request.env["ir.http"]._verify_request_recaptcha_token("signup"):
            raise UserError(_("Suspicious activity detected by Google reCaptcha."))

        return super().passwordless_signup()
