from odoo import fields, models


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
