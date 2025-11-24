import base64
import csv
import io

from odoo import exceptions, fields, models, _
from odoo.tools.translate import _


class FileUploadWizard(models.TransientModel):
    _name = "file.upload.wizard"

    template_id = fields.Many2one(
        comodel_name="subscription.import.template",
        string="Template",
        required=True,
    )
    file_data = fields.Binary("File", required=True)

    def _split_lines_by_model(self, row):
        self.ensure_one()
        lines_by_model = {
            "res.partner": {"create": [], "search": []},
            "sale.subscription": {"create": [], "search": []},
            "product.product": {"create": [], "search": []},
            "sale.subscription.line": {"create": [], "search": []},
        }

        for col_name, cell_value in row.items():
            template_lines = self.template_id.line_ids.filtered(
                lambda l: l.csv_column_name == col_name
            )
            for line in template_lines:
                model_name = line.field_name.model
                field_name = line.field_name.name
                if model_name not in lines_by_model:
                    lines_by_model[model_name] = {"create": [], "search": []}
                lines_by_model[model_name]["create"].append((field_name, cell_value))
                if line.is_search_field and cell_value:
                    lines_by_model[model_name]["search"].append(
                        (field_name, cell_value)
                    )

        return lines_by_model

    def create_records_from_file(self):
        if not self.file_data:
            raise exceptions.UserError(_("Tiedostoa ei ole ladattu."))

        file_data = base64.b64decode(self.file_data)
        file_stream = io.StringIO(file_data.decode("utf-8"))
        rows = list(csv.DictReader(file_stream, delimiter=","))

        for row in rows:
            if not any(row.values()):
                continue

            lines_by_model = self._split_lines_by_model(row)

            partner_create_vals = dict(lines_by_model["res.partner"]["create"])
            partner_search_vals = dict(lines_by_model["res.partner"]["search"])

            partner = False
            if partner_search_vals:
                partner_domain = [
                    (field_name, "=", value)
                    for field_name, value in partner_search_vals.items()
                ]
                partner = self.env["res.partner"].search(partner_domain, limit=1)

            if not partner and partner_create_vals:
                partner = self.env["res.partner"].create(partner_create_vals)
            if not partner:
                continue

            product_create_vals = dict(lines_by_model["product.product"]["create"])
            product_search_vals = dict(lines_by_model["product.product"]["search"])

            product = False
            if product_search_vals:
                product_domain = [
                    (field_name, "=", value)
                    for field_name, value in product_search_vals.items()
                ]
                product = self.env["product.product"].search(product_domain, limit=1)

            if not product and product_create_vals:
                product = self.env["product.product"].create(product_create_vals)

            subscription_create_vals = dict(
                lines_by_model["sale.subscription"]["create"]
            )
            subscription_search_vals = dict(
                lines_by_model["sale.subscription"]["search"]
            )

            subscription = False
            if subscription_search_vals:
                subscription_domain = [
                    (field_name, "=", value)
                    for field_name, value in subscription_search_vals.items()
                ]
                subscription = self.env["sale.subscription"].search(
                    subscription_domain, limit=1
                )

            if not subscription:
                if not subscription_create_vals:
                    continue
                subscription_create_vals.setdefault("partner_id", partner.id)
                subscription = self.env["sale.subscription"].create(
                    subscription_create_vals
                )

            if subscription:
                subscription_line_values = {
                    "sale_subscription_id": subscription.id,
                    "product_id": product.id if product else False,
                }

                self.env["sale.subscription.line"].create(subscription_line_values)

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }
