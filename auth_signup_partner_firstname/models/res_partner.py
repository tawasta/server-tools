from odoo import api, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def signup_retrieve_info(self, token):
        """
        Get the first and lastname from partner record, so they can be shown
        when partner follows the email invitation link
        """
        partner = self._signup_retrieve_partner(token, raise_exception=True)

        res = super().signup_retrieve_info(token)

        if partner.signup_valid:
            res["helper_firstname"] = partner.firstname
            res["helper_lastname"] = partner.lastname

        return res
