from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    fastapi_rest_log_cleanup_whole_line_days = fields.Integer()
    fastapi_rest_log_cleanup_response = fields.Integer()
