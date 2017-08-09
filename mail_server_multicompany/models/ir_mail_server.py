# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
import logging
_logger = logging.getLogger(__name__)


class IrMailserver(models.Model):
    # 1. Private attributes
    _inherit = 'ir.mail_server'

    # 2. Fields declaration
    company = fields.Many2one('res.company', 'Company')

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
    @api.model
    def send_email(self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False):

        if not mail_server_id:
            _logger.info('No mail_server_id. Trying to guess one')
            mail_server_model = self.env['ir.mail_server']

            # Use mail message id meta information for getting the sending company
            # TODO: could this be done with more reliable way?
            references = message['Message-Id']

            # Remove the hostname part
            try:
                references = references.split("@")[0]
            except Exception, e:
                _logger.warning(e)

            references_list = references.split("-")

            if len(references_list) > 3:
                _logger.info('Using Message-Id for matching')

                # The default case where we do get the instance id and model
                # Split the parts to a list. The list should look like this:
                # ['<1490169823.917293071746826.735164174278517', 'openerp', '1234', 'crm.claim']
                # [{id-numbers that we don't use here}, {static 'openerp'}, {model instance id}, {model}]
                model_instance_id = references_list[2]
                model_name = references_list[3]
            else:
                _logger.info('Using sender for matching')
                model_instance_id = False
                model_name = False

                # No known instance id or model. Try to find the server via sender address
                try:
                    from_email = message['From']
                    email_regex = re.compile("[\w\.-]+@[\w\.-]+")
                    email_raw = email_regex.findall(from_email)[0].lower()
                    _logger.info('Trying to find a server for "%s"' % email_raw)
                    ir_mail_server = mail_server_model.search([
                        ('smtp_user', '=', email_raw)
                    ], limit=1)

                    if ir_mail_server:
                        _logger.info('Found server. Using %s' % ir_mail_server.name)
                        mail_server_id = ir_mail_server.id
                    else:
                        _logger.info('No server found. Using the default outgoing server if one is set.')
                except Exception, e:
                    _logger.warning(e)

            if model_name and model_instance_id:
                # Try to find the model instance
                try:
                    model = self.env[model_name]
                    model_instance = model.browse([int(model_instance_id)])

                    # Try different field names
                    if hasattr(model_instance, 'company_id'):
                        company_id = company = getattr(model_instance, 'company_id').id
                    elif hasattr(model_instance, 'company'):
                        company_id = getattr(model_instance, 'company').id
                    else:
                        company_id = False

                except Exception, e:
                    _logger.warning(e)
                    company_id = False

                # Get a company-specific mail server if one exists
                mail_server = mail_server_model.search([
                    ('company', '=', company_id)
                ], limit=1, order='sequence DESC')

                if mail_server:
                    mail_server_id = mail_server.id

        return super(IrMailserver, self).send_email(
            message, mail_server_id, smtp_server, smtp_port,
            smtp_user, smtp_password, smtp_encryption, smtp_debug)