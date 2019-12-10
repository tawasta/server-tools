from odoo import fields, models


class AuthOAuthProvider(models.Model):
    _inherit = 'auth.oauth.provider'

    hd = fields.Char(
        string='Limit login to domain',
        help='E.g. "example.com"',
    )
