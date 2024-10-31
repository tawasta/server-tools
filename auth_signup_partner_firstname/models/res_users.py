from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    def _create_user_from_template(self, values):
        """
        Remove the helper fields from submitted registration form.
        partner_firstname handles formulating the firstname and lastname
        from the full name.
        """

        values.pop("helper_firstname", None)
        values.pop("helper_lastname", None)

        return super()._create_user_from_template(values)
