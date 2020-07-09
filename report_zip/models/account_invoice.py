import base64
import zipfile
import io

from odoo import api, models


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    @api.multi
    def to_zip(self, records, archive_name):
        model_name = "account.account_invoices"
        in_memory_zip = io.BytesIO()
        pdf_list = []
        for record in records:
            file_name = "{} - {} - {}.{}".format(
                record._get_report_base_filename(), record.id, record.name, "pdf"
            )

            pdf_list.append({
                "name": file_name,
                "data": self.env.ref(model_name).sudo().render_qweb_pdf([record.id])[0]
            })

        with zipfile.ZipFile(in_memory_zip, "a") as zip_archive:
            for pdf in pdf_list:
                zip_archive.writestr(pdf['name'], data=pdf['data'])

        archive_attachment = (
            self.env["ir.attachment"]
            .sudo()
            .create(
                {
                    "name": "{}-{}.{}".format("temporary", archive_name, "zip"),
                    "public": False,
                    "datas": base64.b64encode(in_memory_zip.getvalue()),
                    "type": "binary",
                }
            )
        )

        return {
            "type": "ir.actions.act_url",
            "url": archive_attachment.local_url,
        }
