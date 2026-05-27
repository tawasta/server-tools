from odoo import api, fields, models


class GenericImportTemplate(models.Model):
    _name = "generic.import.template"
    _description = "Generic import template"

    name = fields.Char(string="Template Name", required=True)

    step_line_ids = fields.One2many(
        comodel_name="generic.import.template.step",
        inverse_name="template_id",
        string="Import steps",
    )

    step_ids = fields.Many2many(
        comodel_name="generic.import.step",
        compute="_compute_step_ids",
        store=False,
        string="Import steps",
    )

    allowed_model_ids = fields.Many2many(
        comodel_name="ir.model",
        compute="_compute_allowed_model_ids",
        store=False,
        help="Models allowed for mapping, based on selected template steps.",
    )

    line_ids = fields.One2many(
        comodel_name="generic.import.template.line",
        inverse_name="template_id",
        string="Field mappings",
    )

    state_link_ids = fields.One2many(
        comodel_name="generic.import.template.state.link",
        inverse_name="template_id",
        string="State links",
    )

    @api.depends("step_line_ids.step_id")
    def _compute_step_ids(self):
        for tmpl in self:
            tmpl.step_ids = tmpl.step_line_ids.mapped("step_id")

    @api.depends(
        "step_line_ids.step_id",
        "step_line_ids.step_id.required_models",
    )
    def _compute_allowed_model_ids(self):
        IrModel = self.env["ir.model"].sudo()

        for tmpl in self:
            names = set()

            for step_line in tmpl.step_line_ids:
                for model_name in (step_line.step_id.required_models or "").split(","):
                    model_name = model_name.strip()
                    if model_name:
                        names.add(model_name)

            tmpl.allowed_model_ids = (
                IrModel.search(
                    [
                        ("model", "in", sorted(names)),
                        ("transient", "=", False),
                    ]
                )
                if names
                else IrModel.browse([])
            )


class GenericImportTemplateStep(models.Model):
    _name = "generic.import.template.step"
    _description = "Generic import template step"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)

    template_id = fields.Many2one(
        comodel_name="generic.import.template",
        string="Template",
        required=True,
        ondelete="cascade",
    )

    step_id = fields.Many2one(
        comodel_name="generic.import.step",
        string="Step",
        required=True,
        ondelete="cascade",
    )

    code = fields.Char(
        related="step_id.code",
        string="Code",
        readonly=True,
    )

    required_models = fields.Char(
        related="step_id.required_models",
        string="Required Models",
        readonly=True,
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
        if self.field_id and self.model_id and self.field_id.model_id != self.model_id:
            self.field_id = False


class GenericImportTemplateStateLink(models.Model):
    _name = "generic.import.template.state.link"
    _description = "Generic import template state link"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)

    template_id = fields.Many2one(
        comodel_name="generic.import.template",
        string="Template",
        required=True,
        ondelete="cascade",
    )

    apply_on = fields.Selection(
        selection=[
            ("create", "Create"),
            ("write", "Write"),
        ],
        required=True,
        default="write",
    )

    target_state_key = fields.Char(required=True)

    target_model_id = fields.Many2one(
        comodel_name="ir.model",
        string="Target Model",
        required=True,
        ondelete="cascade",
    )

    target_field_id = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Target Field",
        required=True,
        ondelete="cascade",
        domain="[('model_id', '=', target_model_id), ('ttype', '=', 'many2one')]",
    )

    source_state_key = fields.Char(required=True)

    @api.onchange("target_model_id")
    def _onchange_target_model_id_reset_field(self):
        if (
            self.target_field_id
            and self.target_model_id
            and self.target_field_id.model_id != self.target_model_id
        ):
            self.target_field_id = False
