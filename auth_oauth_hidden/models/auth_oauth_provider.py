
# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class AuthOAuthProvider(models.Model):
    # 1. Private attributes
    _inherit = 'auth.oauth.provider'

    # 2. Fields declaration
    hidden = fields.Boolean(
        string='Hide from login',
        help='Only shown is hidden key is provided on address bar',
    )

    hidden_key = fields.Char(
        string='Hidden key',
        help='If the OAuth provider is hidden, providing this in url will show'
        + 'the login button. E.g. "..web/login?key=mykey"',
    )

    # 3. Default methods

    # 4. Compute and search fields

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
