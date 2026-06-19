# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SubscriptionImportTemplateLine(models.Model):
    _name = "subscription.import.template.line"
    _description = "Subscription & contact import template line"

    sequence = fields.Integer(string="Sequence")

    # 2. Fields declaration
    template_id = fields.Many2one(
        comodel_name="subscription.import.template",
        string="Template",
        required=True,
    )

    model_group = fields.Many2one(
        comodel_name="ir.model",
        string="Model",
        required=True,
        domain="[('model', 'in', ['res.partner', 'product.product', 'sale.subscription', 'sale.subscription.line'])]",
        ondelete="cascade",
    )

    is_search_field = fields.Boolean(string="Is Search Field", default=False)

    csv_column_name = fields.Char(string="CSV Column Name", required=True)

    field_name = fields.Many2one(string="Field Name", comodel_name="ir.model.fields", required=True, ondelete="cascade", domain="[('model_id', '=', model_group)]",)


    


    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
