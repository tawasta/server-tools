from odoo import api, fields, models


class AuthSignupMassResetPasswordWizard(models.TransientModel):
    _name = 'auth.signup.mass.reset.password.wizard'
    _description = 'Reset passwords'

    user_ids = fields.Many2many(
        comodel_name='res.users',
        default=lambda self: self.env.context.get('active_ids'))

    @api.multi
    def action_mass_reset_passwords(self):
        ResUser = self.env['res.users']
        user_ids = ResUser.browse(self._context['active_ids'])

        user_ids.action_reset_password()
