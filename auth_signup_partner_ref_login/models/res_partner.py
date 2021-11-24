from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def signup_retrieve_info(self, token):

        res = super(ResPartner, self).signup_retrieve_info(token)
        partner = self._signup_retrieve_partner(token, raise_exception=True)
        res = {'db': self.env.cr.dbname}
        if partner.signup_valid:
            res['token'] = token
            res['name'] = partner.name
        if partner.user_ids:
            res['login'] = partner.user_ids[0].login
            res['email'] = res['email'] = partner.email
        else:
            res['email'] = res['email'] = partner.email
            res['login'] = res['login'] = partner.ref or ''
        return res
