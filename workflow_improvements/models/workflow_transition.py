
# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class WorkflowTransition(models.Model):
    
    # 1. Private attributes
    _inherit = 'workflow.transition'

    # 2. Fields declaration
    act_from_wkf = fields.Char(
        "Workflow",
        compute='compute_act_from_wkf',
        store=False,
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.multi
    def compute_act_from_wkf(self):
        for record in self:
            record.act_from_wkf = record.act_from.wkf_id.name

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
