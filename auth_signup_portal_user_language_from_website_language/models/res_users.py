from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    def _create_user_from_template(self, values):
        # If user creation originates from website, pull the language from context
        # so it contains the selection the user had made in the website's language
        # picker. This overrides whatever language is set in the portal user template.

        res = super()._create_user_from_template(values)

        if self._context.get("website_id") and self._context.get("lang"):
            res.lang = self._context.get("lang")

        return res
