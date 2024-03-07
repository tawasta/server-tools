from odoo import models, fields
from odoo.exceptions import ValidationError

class InstructionMessage(models.Model):
    _name = 'instruction.message'
    _description = 'Instruction Message'

    name = fields.Char('Name')
    model_id = fields.Many2one('ir.model', string='Model', help='The model to which this message is linked.')
    view_id = fields.Many2one('ir.ui.view', string='View', domain=[('type', '=', 'qweb')], help='The QWeb view to which this message is linked.')
    html_content = fields.Html('Message Content', sanitize=True)
    category = fields.Selection([
        ('admin', 'Administration'),
        ('portal', 'Portal')
    ], string='Category', help='The category of the instruction message.', default='admin')
