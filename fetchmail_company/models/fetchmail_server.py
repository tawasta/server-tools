from odoo import models
from odoo import fields


class FetchmailServer(models.Model):

    _inherit = "fetchmail.server"

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
    )
