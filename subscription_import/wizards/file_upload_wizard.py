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
        required=False,
    )
    file_data = fields.Binary("File", required=False)

    def _split_lines_by_model(self, row):
        """
        Splits a CSV row into model-specific create/search data
        based on the selected import template.

        Result structure example:
        {
            'res.partner': {
                'create': [(field, value), ...],
                'search': [(field, value), ...]
            },
            'product.product': {...},
            ...
        }
        """
        self.ensure_one()

        # Initial structure for supported models
        lines_by_model = {
            "res.partner": {"create": [], "search": []},
            "sale.subscription": {"create": [], "search": []},
            "product.product": {"create": [], "search": []},
            "sale.subscription.line": {"create": [], "search": []},
        }
        # Loop through each column in the CSV row
        for col_name, cell_value in row.items():
            # Find matching template lines for this CSV column
            template_lines = self.template_id.line_ids.filtered(
                lambda l: l.csv_column_name == col_name
            )
            # Map CSV value to correct model + field
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
        """
        Main import method. Reads the CSV file and:
        - Create or finds partners
        - Create or finds products
        - Create subscriptions and lines
        - Handles child contacts using Tyyppi column
        """
        if not self.file_data:
            raise exceptions.UserError(_("Tiedostoa ei ole ladattu."))

        file_data = base64.b64decode(self.file_data)
        file_stream = io.StringIO(file_data.decode("utf-8"))
        rows = list(csv.DictReader(file_stream, delimiter=","))

        main_partner = False

        for row in rows:
            if not any(row.values()):
                continue

            # Determine if this row is a child contact
            row_type = (row.get("Tyyppi") or "").strip().lower()
            is_child = row_type == "child"

            lines_by_model = self._split_lines_by_model(row)
            # -------- PARTNER HANDLING --------
            partner_create_vals = dict(lines_by_model["res.partner"]["create"])
            partner_search_vals = dict(lines_by_model["res.partner"]["search"])

            # If this is a child row, link to main partner
            if is_child and main_partner:
                partner_search_vals = {}
                partner_create_vals.setdefault("parent_id", main_partner.id)

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

            if not is_child:
                main_partner = partner

            if is_child:
                continue

            # -------- PRODUCT HANDLING --------
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

            # -------- SUBSCRIPTION HANDLING --------
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
            
            # -------- SUBSCRIPTION LINE CREATION --------

            if subscription:
                line_create_vals = dict(
                    lines_by_model["sale.subscription.line"]["create"]
                )
                line_create_vals.setdefault("sale_subscription_id", subscription.id)
                if product:
                    line_create_vals.setdefault("product_id", product.id)

                self.env["sale.subscription.line"].create(line_create_vals)

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }
