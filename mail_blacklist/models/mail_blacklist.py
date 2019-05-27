
# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class MailBlacklist(models.Model):
    # 1. Private attributes
    _name = 'mail.blacklist'

    # 2. Fields declaration
    name = fields.Char(
        string='Email address or domain'
    )
    description = fields.Text(
        string='Description (e.g. reason this address is on the list',
    )
    type = fields.Selection(
        [('blacklist', 'Blacklist'), ('whitelist', 'Whitelist')]
    )
    direction = fields.Selection(
        [('outgoing', 'Outgoing'), ('incoming', 'Incoming'), ('both', 'Both')],
        'Blacklist type', required=True)

    # 3. Default methods

    # 4. Compute and search fields

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
