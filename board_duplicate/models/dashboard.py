# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models, tools

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ResUsers(models.Model):

    # 1. Private attributes
    # This defines what model you are adding the new fields to
    _inherit = 'res.users' 

    @api.model
    def create(self, values):
        user = super(ResUsers, self).create(values)

        dashboard_template_user_id = 2 

        args = [('user_id', '=', dashboard_template_user_id)]
        dashboard_ids = self.env['ir.ui.view.custom'].search(args)

        for dashboard in dashboard_ids:
            dashboard_copy = dashboard.copy()
            dashboard_copy.user_id = user.id

        return user

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
