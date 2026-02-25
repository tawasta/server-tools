import base64
import csv
import io
import os

from odoo import _, exceptions, fields, models

try:
    from openpyxl import load_workbook
except Exception:
    load_workbook = None


class FileUploadWizard(models.TransientModel):
    _name = "file.upload.wizard"
    _description = "File Upload Wizard"

    template_id = fields.Many2one(
        comodel_name="generic.import.template",
        string="Template",
    )
    file_data = fields.Binary("File")
    file_name = fields.Char("Filename")

    # -------------------------------------------------------------------------
    # File readers
    # -------------------------------------------------------------------------

    def _read_rows_from_csv(self, file_bytes: bytes) -> list[dict]:
        # Keep CSV behaviour as-is (works for you already)
        try:
            text = file_bytes.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = file_bytes.decode("latin-1")

        file_stream = io.StringIO(text)
        return list(csv.DictReader(file_stream, delimiter=","))

    def _read_rows_from_xlsx(self, file_bytes: bytes) -> list[dict]:
        if load_workbook is None:
            raise exceptions.UserError(
                _("XLSX import requires python dependency 'openpyxl'.")
            )

        wb = load_workbook(
            filename=io.BytesIO(file_bytes), data_only=True, read_only=True
        )
        ws = wb.worksheets[0]  # first sheet

        rows_iter = ws.iter_rows(values_only=True)
        try:
            header_row = next(rows_iter)
        except StopIteration:
            return []

        headers = []
        for h in header_row:
            headers.append(str(h).strip() if h is not None else "")

        if not any(headers):
            raise exceptions.UserError(
                _("XLSX file has no header row (first row is empty).")
            )

        result = []
        for row in rows_iter:
            if row is None:
                continue

            data = {}
            any_value = False

            for idx, col_name in enumerate(headers):
                if not col_name:
                    continue

                val = row[idx] if idx < len(row) else None
                if val is None:
                    data[col_name] = ""
                    continue

                if isinstance(val, str):
                    data[col_name] = val.strip()
                else:
                    data[col_name] = str(val).strip()

                if data[col_name] not in ("", None, False):
                    any_value = True

            if any_value:
                result.append(data)

        return result

    def _is_xlsx(self, file_bytes: bytes) -> bool:
        # XLSX is a ZIP container -> magic bytes PK\x03\x04
        return file_bytes[:4] == b"PK\x03\x04"

    def _read_rows_from_file(self) -> list[dict]:
        self.ensure_one()

        if not self.file_data:
            raise exceptions.UserError(_("Tiedostoa ei ole ladattu."))

        file_bytes = base64.b64decode(self.file_data)

        # Detect XLSX by content first (filename may be empty/missing extension)
        if self._is_xlsx(file_bytes):
            return self._read_rows_from_xlsx(file_bytes)

        # Fallback to extension if available
        name = (self.file_name or "").strip().lower()
        root, ext = os.path.splitext(name)  # <-- FIX F823: don't assign to "_"
        if ext == ".xlsx":
            return self._read_rows_from_xlsx(file_bytes)

        return self._read_rows_from_csv(file_bytes)

    # -------------------------------------------------------------------------
    # Mapping helpers
    # -------------------------------------------------------------------------

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
                lambda li, col=col_name: li.csv_column_name == col  # <-- FIX B023
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

    # -------------------------------------------------------------------------
    # Main
    # -------------------------------------------------------------------------

    def create_records_from_file(self):
        self.ensure_one()

        if not self.template_id:
            raise exceptions.UserError(_("Template is required."))

        rows = self._read_rows_from_file()
        if not rows:
            raise exceptions.UserError(_("The uploaded file contains no data rows."))

        steps = self.template_id.step_ids.sorted(key=lambda s: (s.sequence, s.id))
        if not steps:
            raise exceptions.UserError(
                _("Templatelta puuttuu Import steps -määrittely.")
            )

        state = {}

        for row_index, row in enumerate(rows, start=2):
            if not any(row.values()):
                continue

            state.pop("_skip_rest", None)
            lines_by_model = self._split_lines_by_model(row)

            for step in steps:
                if not step.models_installed():
                    continue

                state = (
                    self.env["generic.import.runner"].run_step(
                        step.code, row_index, row, lines_by_model, state
                    )
                    or state
                )

                if state.get("_skip_rest"):
                    break

        return {"type": "ir.actions.client", "tag": "reload"}
