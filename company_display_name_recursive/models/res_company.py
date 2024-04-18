from odoo import api, models


class Company(models.Model):
    _inherit = "res.company"

    def name_get(self):
        result = super().name_get()
        new_result = []

        for res in result:
            company = self.browse(res[0])
            if company.parent_id:
                # name = "{}, {}".format(company.parent_id.display_name, res[1])
                name = self._get_recursive_name(company)
            else:
                name = res[1]
            new_result.append((company.id, name))
        return new_result

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        # Search company name from parent.
        # Please note that this search isn't currently recursive
        res = super().name_search(name=name, args=args, operator=operator)
        if name:
            domain = [
                "|",
                ("name", "ilike", name),
                ("parent_id.name", "ilike", name),
            ]

            args = (args or []) + [
                "|",
                ("name", operator, name),
                ("parent_id.name", operator, name),
            ]

            companies = self.search(domain + (args or []), limit=limit)
            res = companies.name_get()

        return res

    def _get_recursive_name(self, record):
        # Returns a recursive company name

        if record.parent_id and record.parent_id.id != 1:
            display_name = "{} / {}".format(
                self._get_recursive_name(record.parent_id),
                record.name,
            )
        else:
            display_name = record.name

        return display_name
