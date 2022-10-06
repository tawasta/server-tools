##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:

# 2. Known third party imports:
# 3. Odoo imports (openerp):
from odoo import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class View(models.Model):
    # 1. Private attributes
    _inherit = "ir.ui.view"

    # 2. Fields declaration
    xml_id = fields.Char(search="_search_xml_id")
    module = fields.Char(related="model_data_id.module", readonly=True)
    module_is_installed = fields.Boolean(
        compute="_compute_module_is_installed", store=True, readonly=True
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
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

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
