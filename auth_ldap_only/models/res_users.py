from odoo import api, models
from odoo import SUPERUSER_ID
from odoo.exceptions import AccessDenied


class ResUsers(models.Model):
    _inherit = "res.users"

    def check_credentials(self, password):
        if self._uid == SUPERUSER_ID or self.has_group("auth_ldap_only.ldap_bypass"):
            """
            Use normal login process for
            - Admin to prevent locking everyone out
            - Users that belongs to "Bypass LDAP"-group
            """
            return super(ResUsers, self).check_credentials(password=password)
        else:
            raise AccessDenied()
