# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp import tools

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
import logging
_logger = logging.getLogger(__name__)


class IrMailserver(models.Model):
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
    def send_email(self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False):

        # Block outgoing mails if they have blacklisted addresses

        # Get the blacklist
        blacklist_obj = self.env['mail.blacklist']
        blacklist_items = blacklist_obj.sudo().search([])

        blacklist = []
        for blacklist_item in blacklist_items:
            blacklist.append(blacklist_item.name)

        email_list = []

        if message['To']:
            email_list += message['To'].split(",")
        if message['Cc']:
            email_list += message['Cc'].split(",")
        if message['Bcc']:
            email_list += message['Bcc'].split(",")

        for email in email_list:
            try:
                address = tools.email_split(email)[0]
            except IndexError:
                address = False
                _logger.warn('Invalid email: "%s"', email)

            if address and any(address in s for s in blacklist):
                _logger.warning("'%s' is blacklisted! Did not send mail", email)
                return False

        return super(IrMailserver, self).send_email(
            message, mail_server_id, smtp_server, smtp_port,
            smtp_user, smtp_password, smtp_encryption, smtp_debug)