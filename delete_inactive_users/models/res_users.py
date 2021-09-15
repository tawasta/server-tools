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
