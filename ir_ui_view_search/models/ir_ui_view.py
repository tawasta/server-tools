from odoo import api, fields, models


class View(models.Model):
    _inherit = "ir.ui.view"

    xml_id = fields.Char(search="_search_xml_id")
    module = fields.Char(related="model_data_id.module", readonly=True)
    module_is_installed = fields.Boolean(
        compute="_compute_module_is_installed", store=True, readonly=True
    )

    def _search_xml_id(self, operator, value):
        domain = [
            ("model", "=", "ir.ui.view"),
            "|",
            "|",
            ("module", operator, value),
            ("name", operator, value),
            ("res_id", operator, value),
        ]
        data = self.env["ir.model.data"].sudo().search(domain)
        return [("id", "in", data.mapped("res_id"))]

    @api.depends("module")
    def _compute_module_is_installed(self):
        for view in self:
            module_search = (
                self.env["ir.module.module"]
                .sudo()
                .search(
                    [
                        ("name", "=", view.module),
                        ("state", "in", ["installed", "to upgrade", "to remove"]),
                    ]
                )
            )
            if module_search:
                view.module_is_installed = True
            else:
                view.module_is_installed = False
