# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SubscriptionImportTemplate(models.Model):
    _name = "subscription.import.template"
    _description = "Subscription & contact import configuration"

    # 2. Fields declaration
    name = fields.Char(string="Template Name", required=True)

    line_ids = fields.One2many(
        comodel_name="subscription.import.template.line",
        inverse_name="template_id",
        string="Template Lines",
    )

    


    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
