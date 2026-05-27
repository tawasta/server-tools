from odoo import api, fields, models


class GenericImportStep(models.Model):
    _name = "generic.import.step"
    _description = "Generic import step"
    _order = "sequence, id"

    name = fields.Char(required=True)
    code = fields.Char(
        required=True,
        help="Dispatch key, e.g. partner, product, event, sale",
    )
    sequence = fields.Integer(default=10)

    required_models = fields.Char(
        help="Comma-separated required model names, e.g. res.partner,product.template"
    )

    @api.model
    def models_installed(self) -> bool:
        if not self.required_models:
            return True

        installed = set(self.env.registry.keys())
        needed = [
            m.strip() for m in (self.required_models or "").split(",") if m.strip()
        ]
        return all(m in installed for m in needed)
