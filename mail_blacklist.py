from openerp.osv import osv, fields

class mail_blacklist(osv.Model):
    _name = 'mail.blacklist'
    
    _columns = {
        'name': fields.char('Email address or domain'),
        'description': fields.text('Description (e.g. reason this address is on the list'),
        'type': fields.selection( (('outgoing','Outgoing'), ('incoming', 'Incoming')) , 'Blacklist type', required=True),
    }