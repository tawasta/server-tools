# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class WorkflowWorkitem(models.Model):
    
    # 1. Private attributes
    _inherit = 'workflow.workitem'

    # 2. Fields declaration
    instance_resource_id = fields.Integer("Resource id", compute='compute_instance_resource_id')

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.multi
    def compute_instance_resource_id(self):
        for record in self:
            record.instance_resource_id = record.inst_id.res_id

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
