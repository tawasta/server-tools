from odoo import models
from odoo.exceptions import AccessDenied


class Users(models.Model):
    _inherit = "res.users"

    def _check_credentials(self, password):
        try:
            if self._uid in [1, 2] or self.has_group(
                "auth_ldap_only.ldap_bypass"
            ):
                """
                Use normal login process for
                - Admin to prevent locking everyone out
                - Users that belongs to "Bypass LDAP"-group
                """
                super(Users, self)._check_credentials(password)
            else:
                # Raise AccessDenied to try LDAP login
                raise AccessDenied
        except AccessDenied:
            # LDAP Login
            if self.env.user.active:
                Ldap = self.env["res.company.ldap"]
                for conf in Ldap._get_ldap_dicts():
                    if Ldap._authenticate(conf, self.env.user.login, password):
                        return
            raise
