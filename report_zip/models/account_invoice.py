import base64
import io
import logging
import zipfile

from odoo import _, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def to_zip(self, records, archive_name):
        """Luo ZIP-tiedoston laskujen PDF-tulosteista ja palauttaa latauslinkin."""

        if not records:
            raise UserError(_("No invoices selected."))

        try:
            # Luo muistissa oleva ZIP-tiedosto
            in_memory_zip = io.BytesIO()

            # Haetaan kaikki PDF:t yhdellä kutsulla (tehokkaampaa)
            pdf_report = self.env["ir.actions.report"]
            pdf_data_map = {
                invoice.id: pdf_report._render_qweb_pdf(
                    "account.account_invoices", res_ids=invoice.id
                )[0]
                for invoice in records
            }

            with zipfile.ZipFile(
                in_memory_zip, "w", zipfile.ZIP_DEFLATED
            ) as zip_archive:
                for invoice in records:
                    file_name = f"{invoice.name.replace('/', '-')}.pdf"
                    zip_archive.writestr(file_name, pdf_data_map[invoice.id])

            # Luodaan ZIP-tiedosto attachmentiksi
            attachment = (
                self.env["ir.attachment"]
                .sudo()
                .create(
                    {
                        "name": f"{archive_name}.zip",
                        "type": "binary",
                        "datas": base64.b64encode(in_memory_zip.getvalue()),
                        "public": False,
                    }
                )
            )

            return {
                "type": "ir.actions.act_url",
                "url": f"/web/content/{attachment.id}?download=true",
                "target": "self",
            }

        except Exception as e:
            logging.error(f"Failed to create ZIP file: {e}")
            raise UserError(_("An error occurred while creating the ZIP file.")) from e
