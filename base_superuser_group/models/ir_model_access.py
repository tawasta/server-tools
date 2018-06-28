# -*- coding: utf-8 -*-

from odoo import api, models, tools


class IrModelAccess(models.Model):
    _inherit = 'ir.model.access'

    @api.model
    @tools.ormcache_context(
        'self._uid', 'model', 'mode', 'raise_exception', keys=('lang',)
    )
    def check(self, model, mode='read', raise_exception=True):

        if self.env.user.has_group('base_superuser_group.superuser'):
            return True

        return super(IrModelAccess, self).check(
            model=model,
            mode=mode,
            raise_exception=raise_exception,
        )
