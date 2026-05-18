import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    def _create_user_from_template(self, values):
        values.pop("recaptcha_token_response", None)

        return super()._create_user_from_template(values)
