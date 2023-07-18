from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    inactive_users = fields.Integer(
        config_parameter="delete_inactive_users.inactive_users",
    )
