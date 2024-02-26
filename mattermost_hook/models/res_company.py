from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    mattermost_hook_ids = fields.One2many(
        comodel_name="mattermost.hook",
        inverse_name="company_id",
        string="Company mattermost hooks",
        help="Mattermost hooks used by this company",
    )
