from odoo import api, models, fields, exceptions
import logging

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    def action_reset_password(self):
        # OCA's auth_signup_verify_email uses the reset password functionality for
        # sending the invitation.
        # Clear the origin URL field after initial sending so that it does not get
        # used in subsequent actual password reset emails

        res = super().action_reset_password()

        for user in self:
            user.partner_id.portal_user_signup_origin_url = False

        return res
