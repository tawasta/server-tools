from odoo import models, fields


class RedirectRule(models.Model):

    _name = 'base_simple_urls.redirect_rule'
    _description = 'Redirect Rule'

    get_variable = fields.Char(
        string='GET Variable',
        required=True
    )

    model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Target model',
        required=True
    )

    field_id = fields.Many2one(
        comodel_name='ir.model.fields',
        string='Target field',
        required=True
    )

    action_id = fields.Many2one(
        comodel_name='ir.actions.act_window',
        string='Target action',
        required=True
    )

    description = fields.Char('Description')

    _sql_constraints = [
        ('get_variable',
         'unique(get_variable)',
         'Please use a unique GET variable')
    ]
