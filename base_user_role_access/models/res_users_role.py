# -*- coding: utf-8 -*-
from odoo import models, api


class ResUsersRole(models.Model):

    _inherit = 'res.users.role'

    @api.multi
    def action_access_right_tree(self):
        action = self.env.ref(
            'base.ir_access_act') \
            .read()[0]

        domain = [
            '|',
            ('group_id', 'in', self.implied_ids.ids),
            ('group_id', '=', False),
        ]

        action['domain'] = domain

        return action
