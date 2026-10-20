import datetime
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class FastapiRestLog(models.Model):
    _name = "fastapi.rest.log"
    _description = "FastAPI REST Log"
    _order = "create_date desc"

    method = fields.Char(required=True, index=True)
    path = fields.Char(required=True, index=True)
    odoo_user_id = fields.Many2one("res.users", string="Odoo User", index=True)
    payload = fields.Text(string="Request Payload")
    response = fields.Text(string="Response Payload")
    status_code = fields.Integer(index=True)
    ip_address = fields.Char(string="Client IP", index=True)

    def action_cleanup(self):
        if self.create_date:
            now = datetime.datetime.now()

            full_clean_days = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("fastapi_rest_log_cleanup_whole_line_days", default="180")
            )
            if fields.DateTime.to_datetime(self.create_date) < now - datetime.timedelta(
                days=full_clean_days
            ):
                self.unlink()
                return

            response_clean_days = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("fastapi_rest_log_response_cleanup_days", default="90")
            )
            if fields.DateTime.to_datetime(self.create_date) < now - datetime.timedelta(
                days=response_clean_days
            ):
                self.write({"response": ""})
