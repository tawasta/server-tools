# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp import tools
from openerp import _

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

        MailBlacklist = self.env['mail.blacklist']

        # Get the whitelist
        whitelist = list()
        whitelist_items = MailBlacklist.sudo().search([('type', '=', 'whitelist')])

        for whitelist_item in whitelist_items:
            whitelist.append(whitelist_item.name)

        if whitelist:
            _logger.debug("Whitelist: %s", (', '.join(whitelist)))

        # Get the blacklist
        blacklist = list()

        if not whitelist:
            # Don't get blacklist items if there are whitelist items
            blacklist_items = MailBlacklist.sudo().search([('type', '=', 'blacklist')])
            for blacklist_item in blacklist_items:
                blacklist.append(blacklist_item.name)

        if blacklist:
            _logger.debug("Blacklist: %s", (', '.join(blacklist)))

        email_list = list()
        address_regex = re.compile("[\w\.-]+@[\w\.-]+")

        if message['To']:
            email_list += address_regex.findall(message['To'])
        if message['Cc']:
            email_list += address_regex.findall(message['Cc'])
        if message['Bcc']:
            email_list += address_regex.findall(message['Bcc'])

        # Remove duplicates
        email_list = list(set(email_list))

        if email_list:
            _logger.info("Emails: %s", (', '.join(email_list)))

        for email in email_list:
            try:
                address = tools.email_split(email)[0]
                domain = re.search("@[\w.]+", address).group()

            except IndexError:
                address = False
                _logger.warn('Invalid email: "%s"', email)

            errors = list()

            if not address:
                continue

            if whitelist:
                if not any(domain in s for s in whitelist) and not any(address in s for s in whitelist):
                    msg = _("'%s' is not whitelisted! Did not send mail") % email
                    errors.append(msg)

            elif blacklist:
                if address and any(address in s for s in blacklist):
                    msg = _("'%s' is blacklisted! Did not send mail") % email
                    errors.append(msg)

            for error in errors:
                _logger.warning(error)

            if errors:
                return False

        return super(IrMailserver, self).send_email(
            message, mail_server_id, smtp_server, smtp_port,
            smtp_user, smtp_password, smtp_encryption, smtp_debug)