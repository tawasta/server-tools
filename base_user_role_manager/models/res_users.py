from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    role_ids = fields.One2many(
        comodel_name="res.users.role",
        string="User Roles",
        compute="_compute_role_ids",
        compute_sudo=True,
        groups="base.group_erp_manager,base_user_role_manager.group_role_manager",
    )

    role_line_ids = fields.One2many(
        comodel_name="res.users.role.line",
        groups="base.group_erp_manager,base_user_role_manager.group_role_manager",
    )
