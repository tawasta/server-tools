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
import json

# 3. Odoo imports (openerp):
from odoo import models
from odoo.exceptions import AccessDenied
from odoo.http import request

# 2. Known third party imports:

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ResUsers(models.Model):

    # 1. Private attributes
    _inherit = "res.users"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def user_info(self):
        """Return user related data"""
        self.ensure_one()
        # Add webrole and webrole-meta
        vals = {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "login": self.login,
            "email": self.email,
            "membershipnumber": self.partner_id.ref,
        }
        return vals

    def user_info_json(self):
        """Return user data in JSON-format"""
        remote_ip = request.httprequest.remote_addr
        allowed_ips = (
            self.env["ir.config_parameter"].sudo().get_param("idp_allowed_ips", "")
        ).split(",")
        if remote_ip not in allowed_ips:
            raise AccessDenied

        return json.dumps(self.user_info(), ensure_ascii=False)

    # 8. Business methods
