
# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, models
from odoo import registry
from odoo import SUPERUSER_ID
from odoo.exceptions import AccessDenied


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ResUsers(models.Model):
    # 1. Private attributes
    _inherit = 'res.users'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
    @api.model
    def check_credentials(self, password):
        try:
            if self._uid == SUPERUSER_ID or \
                    self.has_group('auth_ldap_only.ldap_bypass'):
                '''
                Use normal login process for
                - Admin to prevent locking everyone out
                - Users that belongs to "Bypass LDAP"-group
                '''
                super(ResUsers, self).check_credentials(password=password)
            else:
                raise AccessDenied()
        except AccessDenied:
            cr = registry().cursor()
            cr.execute(
                'SELECT login FROM res_users WHERE id=%s AND active=TRUE',
                (int(self._uid),)
            )
            res = cr.fetchone()
            cr.close()

            if res:
                Ldap = self.env['res.company.ldap']
                for conf in Ldap.get_ldap_dicts():
                    if Ldap.authenticate(conf, self.env.user.login, password):
                        return
            raise
