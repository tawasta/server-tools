import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):

    _inherit = "res.company"

    @api.model
    def create(self, vals):
        # Find all users who have the autoaccess rights, and add access to the new
        # company for them

        new_company = super().create(vals)

        autoaccess_group = self.env.ref(
            "res_groups_autoaccess_new_companies.group_autoaccess_new_companies"
        )

        users_with_autoaccess = (
            self.env["res.users"]
            .sudo()
            .search([("groups_id", "in", autoaccess_group.id)])
        )

        for user in users_with_autoaccess:
            user.write({"company_ids": [(4, new_company.id)]})

        return new_company
