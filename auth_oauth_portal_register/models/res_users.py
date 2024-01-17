##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2019- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
from odoo import _, api, models

# 4. Imports from Odoo modules:
from odoo.addons.auth_signup.models.res_partner import SignupError

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    # 1. Private attributes
    _inherit = "res.users"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
    @api.model
    def _signup_create_user(self, values):
        """
        Overwrite method to allow registering through OAuth2
        without opening signup form.

        :param values: dict
        :return: method call
        """
        if "oauth_provider_id" not in values and "partner_id" not in values:
            if self._get_signup_invitation_scope() != "b2c":
                raise SignupError(_("Signup is not allowed for uninvited users"))
        _logger.info("#################")
        _logger.info(values)
        return self._create_user_from_template(values)
