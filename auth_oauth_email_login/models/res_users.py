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
import logging

# 3. Odoo imports (openerp):
from odoo import api, models
from odoo.exceptions import AccessDenied, UserError

from odoo.addons.auth_signup.models.res_users import SignupError

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

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.model
    def _auth_oauth_signin(self, provider, validation, params):
        """Allow login with email if no match with oauth_uid"""
        oauth_uid = validation["user_id"]
        email = validation["email"]
        try:
            oauth_user = self.search(
                [
                    "|",
                    "&",
                    ("oauth_uid", "=", oauth_uid),
                    ("oauth_provider_id", "=", provider),
                    ("email", "=ilike", email),
                ]
            )
            if not oauth_user:
                raise AccessDenied()
            assert len(oauth_user) == 1

            oauth_user.write({"oauth_access_token": params["access_token"]})
            if oauth_user.oauth_uid != oauth_uid:
                # Update OAuth UID to user
                _logger.info(
                    "OAuth wasn't matched so we logged in with email {}, "
                    "update oauth data".format(email)
                )
                oauth_user.write(
                    {
                        "oauth_provider_id": provider,
                        "oauth_uid": oauth_uid,
                    }
                )
            return oauth_user.login
        except AccessDenied as access_denied_exception:
            if self.env.context.get("no_user_creation"):
                return None
            state = json.loads(params["state"])
            token = state.get("t")
            values = self._generate_signup_values(provider, validation, params)
            try:
                _, login, _ = self.signup(values, token)
                return login
            except (SignupError, UserError):
                raise access_denied_exception

    # 8. Business methods
