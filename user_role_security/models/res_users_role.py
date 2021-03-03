from odoo import fields
from odoo import models


class ResUsersRole(models.Model):
    _inherit = "res.users.role"

    record_rules_ids = fields.Many2many(
        comodel_name='ir.rule',
        relation='record_rule_rel',
        string='Record rules',
        compute="_get_all_record_rules",
        readonly=True,
    )

    access_rights_ids = fields.Many2many(
        comodel_name='ir.model.access',
        relation='access_rights_rel',
        string='Access Rights',
        compute="_get_all_access_rights",
        readonly=True,
    )

    def _get_all_record_rules(self):
        for record in self:
            implied_ids = record.implied_ids
            all_record_rules = self.env["ir.rule"].sudo().search([
                ('groups', 'in', implied_ids.ids)
            ])
            record.record_rules_ids = all_record_rules

    def _get_all_access_rights(self):
        for record in self:
            implied_ids = record.implied_ids
            all_access_rights = self.env["ir.model.access"].sudo().search([
                ('group_id', 'in', implied_ids.ids)
            ])
            record.access_rights_ids = all_access_rights
