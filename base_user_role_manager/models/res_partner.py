from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    signup_token = fields.Char(
        groups="base.group_erp_manager,base_user_role_manager.group_role_manager"
    )
    signup_type = fields.Char(
        groups="base.group_erp_manager,base_user_role_manager.group_role_manager"
    )
    signup_expiration = fields.Datetime(
        groups="base.group_erp_manager,base_user_role_manager.group_role_manager"
    )
