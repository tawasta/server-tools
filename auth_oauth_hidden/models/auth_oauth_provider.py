from odoo import fields, models


class AuthOAuthProvider(models.Model):
    _inherit = 'auth.oauth.provider'

    hidden = fields.Boolean(
        string='Hide from login',
        help='Only shown is hidden key is provided on address bar',
    )

    hidden_key = fields.Char(
        string='Hidden key',
        help='If the OAuth provider is hidden, providing this in url will show'
        + 'the login button. E.g. "..web/login?key=mykey"',
    )
