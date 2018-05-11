# -*- coding: utf-8 -*-

# 1. Standard library imports:
import logging

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models, _
from odoo.exceptions import AccessDenied


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
_logger = logging.getLogger(__name__)


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
    def _auth_oauth_validate(self, provider, access_token):
        res = super(ResUsers, self)._auth_oauth_validate(
            provider=provider,
            access_token=access_token,
        )

        oauth_provider = self.env['auth.oauth.provider'].browse(provider)

        if oauth_provider.hd and not res.get('hd') == oauth_provider.hd:
            msg = _("'%s' tried to login from outside of the domain"
                    % res.get('email'))
            _logger.warning(msg)
            raise AccessDenied()

        return res