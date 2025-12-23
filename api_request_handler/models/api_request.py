import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ApiRequest(models.Model):
    _name = "api.request"
    _description = "API Request"
    _order = "create_date desc"

    name = fields.Char(compute="_compute_name", store=True)
    method = fields.Selection(
        [
            ("GET", "GET"),
            ("POST", "POST"),
            ("PUT", "PUT"),
            ("DELETE", "DELETE"),
        ]
    )
    endpoint = fields.Char()
    headers = fields.Text()
    params = fields.Text()
    values = fields.Text()
    payload = fields.Text()
    response = fields.Text()
    status_code = fields.Integer()
    successful = fields.Boolean(default=False)
    error_message = fields.Text()

    res_model = fields.Char(string="Related Model", readonly=True)
    res_id = fields.Integer(string="Related Record ID", readonly=True)

    def _compute_name(self):
        for record in self:
            record.name = f"{record.method} {record.endpoint} [{record.status_code}]"

    def action_open_related_record(self):
        self.ensure_one()
        if self.res_model and self.res_id:
            return {
                "type": "ir.actions.act_window",
                "res_model": self.res_model,
                "res_id": self.res_id,
                "view_mode": "form",
            }
        return None
