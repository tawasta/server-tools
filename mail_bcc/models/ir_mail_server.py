# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class IrMailServer(models.Model):

    # 1. Private attributes
    _inherit = 'ir.mail_server'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
    @api.model
    def send_email(self, message, mail_server_id=None, smtp_server=None,
        smtp_port=None, smtp_user=None, smtp_password=None,
        smtp_encryption=None, smtp_debug=False):
        # Send a BCC message to an address every time a mail is sent.
        # This is for debugging purposes

        # Set a BCC recipient. This only works if one is not already set
        message['Bcc'] = "odoo@tawasta.fi"

        return super(IrMailServer, self).send_email(
            message, mail_server_id, smtp_server, smtp_port,
            smtp_user, smtp_password, smtp_encryption, smtp_debug)