# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models, tools

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ViewCustom(models.Model):

    # 1. Private attributes
    # This defines what model you are adding the new fields to
    _name = 'ir.ui.view.custom'
    _inherit = 'ir.ui.view.custom' 

    # 2. Fields declaration

    jotain = fields.Text(string='jotain', required=True)

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
