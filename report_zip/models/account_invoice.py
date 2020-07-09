import base64
import os
import zipfile

from odoo import api, models


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    @api.multi
    def to_zip(self, records, archive_name):
        model_name = "account.account_invoices"
        archive_path = "/tmp/{}.{}".format(archive_name, "zip",)

        with zipfile.ZipFile(archive_path, "w") as zip_archive:
            for record in records:
                pdf_file = self.env.ref(model_name).sudo().render_qweb_pdf([record.id])

                file_name = "{} - {} - {}.{}".format(
                    record._get_report_base_filename(), record.id, record.name, "pdf"
                )

                zip_archive.writestr(
                    file_name, data=pdf_file[0],
                )

        archive_filename = "{}.{}".format(archive_name, "zip",)

        f = open(archive_path, "rb")
        archive_attachment = (
            self.env["ir.attachment"]
            .sudo()
            .create(
                {
                    "name": "{}-{}".format("temporary", archive_filename),
                    "public": False,
                    "datas": base64.b64encode(f.read()),
                    "type": "binary",
                }
            )
        )
        f.close()

        if os.path.isfile(archive_path):
            os.remove(archive_path)

        return {
            "type": "ir.actions.act_url",
            "url": archive_attachment.local_url,
        }
