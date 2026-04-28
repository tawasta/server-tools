import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def signup(self, values, token=None):
        """If partner was set, run commercial partner computation to ensure
        commercial_partner_id reflects the parent_id that got set"""

        # result is in format: (login, password)
        result = super().signup(values, token=token)

        user = self.search([("login", "=", result[0])], limit=1)
        if user.partner_id.parent_id:
            user.partner_id._compute_commercial_partner()

        return result
