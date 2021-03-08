##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2019- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
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

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import models
from odoo.exceptions import AccessDenied


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class ResUsersLog(models.Model):

    # 1. Private attributes
    _inherit = "res.users.log"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def login_statistics(self, start_date, end_date, group_ids=None):
        """
        Method to retrieve user login statistics

        :param start_date: string, date in isoformat
        :param start_date: string, date in isoformat
        :param group_ids: list, list of security group IDs
        :return: int, user count
        """
        if not self.env.user._is_admin():
            raise AccessDenied()

        res = {}
        log_domain = [
            ("create_date", ">=", start_date),
            ("create_date", "<=", end_date),
        ]
        logs = self.sudo().search(log_domain)

        if group_ids:
            groups = self.env["res.groups"].sudo().browse(group_ids)
            for group in groups:
                users = logs.filtered(
                    lambda r: r.create_uid.id in group.users.ids
                ).mapped("create_uid")
                key = "users_{}".format(group.id)
                res[key] = len(users)
        else:
            res["users"] = len(logs.mapped("create_uid"))
        return res

    # 8. Business methods
