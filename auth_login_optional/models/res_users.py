##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
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
import logging

# 3. Odoo imports (openerp):
from odoo import api, models

# 2. Known third party imports:

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


_logger = logging.getLogger(__name__)


class ResUsers(models.Model):

    # 1. Private attributes
    _inherit = "res.users"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.model
    def _get_login_domain(self, login):
        """Get login field from ICP"""
        domain = []
        login_field = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("auth_login_optional.optional_login_field", "")
        )
        if login_field:
            domain = [
                "|",
                "&",
                (login_field, "=", login),
                (login_field, "!=", False),
            ]
        domain.extend(super()._get_login_domain(login))
        return domain

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
