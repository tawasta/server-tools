from openerp.osv import osv
from openerp import tools

import logging
_logger = logging.getLogger(__name__)

class ir_mail_server(osv.Model):
    _inherit = 'ir.mail_server'
    
    def send_email(self, cr, uid, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False,
                   context=None):
        ''' Block outgoing mails if they have blacklisted addresses '''
        
        ''' Get the blacklist '''
        blacklist_obj = self.pool.get('mail.blacklist')
        blacklist_ids = blacklist_obj.search(cr, uid, [('type','=','outgoing')])
        blacklist_items = blacklist_obj.browse(cr, uid, blacklist_ids)
        
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
            address = tools.email_split(email)[0]
            if any(address in s for s in blacklist):
                _logger.warning("'%s' is blacklisted! Did not send mail", email)
                return False
        
        return super(ir_mail_server, self).send_email(cr, uid, message, mail_server_id, smtp_server, smtp_port,
                   smtp_user, smtp_password, smtp_encryption, smtp_debug,
                   context=context)