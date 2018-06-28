# -*- coding: utf-8 -*-

from odoo import api, models


class BaseModelSuperuserGroup(models.AbstractModel):
    _name = 'basemodel.superuser.group'

    @api.model_cr
    def _register_hook(self):

        @api.model
        def do_check_field_access_rights(self, operation, fields, **kw):

            if self.env.user.has_group('base_superuser_group.superuser'):
                return fields or list(self._fields)

            return do_check_field_access_rights.origin(
                self,
                operation=operation,
                fields=fields,
                ** kw
            )

        models.BaseModel._patch_method(
            'check_field_access_rights',
            do_check_field_access_rights
        )

        models.BaseModel.check_field_access_rights = \
            do_check_field_access_rights
        return super(BaseModelSuperuserGroup, self)._register_hook()
