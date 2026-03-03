from odoo import api, fields, models


class GenericImportTemplate(models.Model):
    _name = "generic.import.template"
    _description = "Generic import template"

    name = fields.Char(string="Template Name", required=True)

    step_ids = fields.Many2many(
        comodel_name="generic.import.step",
        relation="generic_import_template_step_rel",
        column1="template_id",
        column2="step_id",
        string="Import steps",
        help="Select steps to run. Steps are provided by installed step modules.",
    )

    # Allowed models computed from selected steps
    allowed_model_ids = fields.Many2many(
        comodel_name="ir.model",
        compute="_compute_allowed_model_ids",
        store=False,
        help="Models allowed for mapping, based on selected steps.",
    )

    line_ids = fields.One2many(
        comodel_name="generic.import.template.line",
        inverse_name="template_id",
        string="Field mappings",
    )

    @api.depends("step_ids", "step_ids.required_models")
    def _compute_allowed_model_ids(self):
        IrModel = self.env["ir.model"].sudo()
        for tmpl in self:
            names = set()
            for step in tmpl.step_ids:
                for m in (step.required_models or "").split(","):
                    m = (m or "").strip()
                    if m:
                        names.add(m)

            # If no steps selected -> no allowed models
            if not names:
                tmpl.allowed_model_ids = IrModel.browse([])
                continue

            # Only installed models exist in ir.model, so this is safe.
            tmpl.allowed_model_ids = IrModel.search(
                [
                    ("model", "in", sorted(names)),
                    ("transient", "=", False),
                ]
            )


class GenericImportTemplateLine(models.Model):
    _name = "generic.import.template.line"
    _description = "Generic import template line"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)

    template_id = fields.Many2one(
        comodel_name="generic.import.template",
        string="Template",
        required=True,
        ondelete="cascade",
    )

    csv_column_name = fields.Char(required=True)
    is_search_field = fields.Boolean(default=False)

    # Domain is set in the view using parent.allowed_model_ids (webclient-safe)
    model_id = fields.Many2one(
        comodel_name="ir.model",
        string="Model",
        required=True,
        ondelete="cascade",
    )

    field_id = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Field",
        required=True,
        ondelete="cascade",
        domain="[('model_id', '=', model_id)]",
    )

    @api.onchange("model_id")
    def _onchange_model_id_reset_field(self):
        # Prevent keeping a field that belongs to another model
        if self.field_id and self.model_id and self.field_id.model_id != self.model_id:
            self.field_id = False
