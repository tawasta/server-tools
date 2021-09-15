from odoo import models
from odoo import api
from datetime import datetime


class ResUsers(models.Model):

    _inherit = "res.users"

    @api.model
    def _delete_users(self):
        get_param = self.env["ir.config_parameter"].sudo().get_param
        inactive_users_val = get_param("delete_inactive_users.inactive_users")
        inactive_users = self.env["res.users"].sudo().search([
            ('log_ids', '=', False)
        ])
        date_now = datetime.now()
        if inactive_users:
            for user in inactive_users:
                days_in_system = date_now.date() - user.create_date.date()
                if int(days_in_system.days) > int(inactive_users_val):
                    user.sudo().write({"active": False})

    @api.model_create_multi
    def create(self, vals_list):
        login_key = "login"
        lastname_key = "lastname"
        firstname_key = "firstname"
        login_of_key = [a_dict[login_key] for a_dict in vals_list]
        lastname_of_key = [a_dict[lastname_key] for a_dict in vals_list]
        firstname_of_key = [a_dict[firstname_key] for a_dict in vals_list]
        already_user_by_email = self.env["res.users"].sudo().search([
            ('login', '=ilike', login_of_key[0]),
            ('lastname', '=ilike', lastname_of_key[0]),
            ('firstname', '=ilike', firstname_of_key[0]),
            ('active', '=', False),
        ])
        if already_user_by_email and already_user_by_email.active == False:
            already_user_by_email.sudo().write({"active": True})
            return already_user_by_email
        else:
            return super(ResUsers, self).create(vals_list)
