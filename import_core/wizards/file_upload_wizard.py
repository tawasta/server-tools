import base64
import csv
import io

from odoo import _, exceptions, fields, models


class FileUploadWizard(models.TransientModel):
    _name = "file.upload.wizard"
    _description = "File Upload Wizard"

    template_id = fields.Many2one(
        comodel_name="generic.import.template",
        string="Template",
    )
    file_data = fields.Binary("File")
    file_name = fields.Char("Filename")

    def _split_lines_by_model(self, row: dict) -> dict:
        """
        Return:
        {
          'res.partner': {'create': [(field,val)], 'search': [(field,val)]},
          ...
        }
        """
        self.ensure_one()
        result = {}

        for col_name, cell_value in row.items():
            tlines = self.template_id.line_ids.filtered(
                lambda li: li.csv_column_name == col_name
            )
            for line in tlines:
                model_name = line.field_id.model
                field_name = line.field_id.name

                # Skip mapping for models not installed
                if model_name not in self.env.registry:
                    continue

                result.setdefault(model_name, {"create": [], "search": []})
                result[model_name]["create"].append((field_name, cell_value))

                if line.is_search_field and cell_value not in ("", None, False):
                    result[model_name]["search"].append((field_name, cell_value))

        return result

    def create_records_from_file(self):
        self.ensure_one()

        if not self.file_data:
            raise exceptions.UserError(_("Tiedostoa ei ole ladattu."))

        file_data = base64.b64decode(self.file_data)
        file_stream = io.StringIO(file_data.decode("utf-8"))
        rows = list(csv.DictReader(file_stream, delimiter=","))

        steps = self.template_id.step_ids.sorted(key=lambda s: (s.sequence, s.id))
        if not steps:
            raise exceptions.UserError(_("Templatelta puuttuu Import steps -määrittely."))

        state = {}

        for row_index, row in enumerate(rows, start=2):
            if not any(row.values()):
                continue

            state.pop("_skip_rest", None)
            lines_by_model = self._split_lines_by_model(row)

            for step in steps:
                if not step.models_installed():
                    continue

                state = self.env["generic.import.runner"].run_step(
                    step.code, row_index, row, lines_by_model, state
                ) or state

                # If a step sets this (e.g. child-row in contacts step), stop remaining steps for this row.
                if state.get("_skip_rest"):
                    break

        return {"type": "ir.actions.client", "tag": "reload"}