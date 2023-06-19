# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.misc import find_in_path

import os
import logging
import subprocess
from tempfile import NamedTemporaryFile

_logger = logging.getLogger(__name__)


# Check the presence of Ghostscript and return it's path
def _get_ghostscript_bin():
    ghostscript_bin = find_in_path("ghostscript")
    if ghostscript_bin is None:
        raise IOError
    return ghostscript_bin


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    pdf_option = fields.Selection(
        string="PDF/A archiving",
        selection=[("no", "None"), ("pdfa1b", "PDF/A-1B")],
        required=True,
        default="no",
        help="PDF/A is an ISO-standardized version of the Portable Document "
        "Format (PDF) specialized for the digital preservation of "
        "electronic documents.",
    )

    # Run ghostscript if pdf/a option is selected
    def render_qweb_pdf(self, res_ids=None, data=None):
        if not self.env.context.get("res_ids") and self.pdf_option != "no":
            pdf = super(
                IrActionsReport, self.with_context(res_ids=res_ids)
            ).render_qweb_pdf(res_ids=res_ids, data=data)
            logging.info("=======TANNE MENEE JA AJAA GHOSTIN=======");
            processed_pdf = self._run_ghostscript(pdf[0])
            return processed_pdf, "pdf"
        return super(IrActionsReport, self).render_qweb_pdf(res_ids=res_ids, data=data)

    # Runs ghostscript to convert pdf into pdf/a
    def _run_ghostscript(self, pdf):

        with NamedTemporaryFile(delete=False, suffix=".pdf") as f1:
            f1.write(pdf)

        f2 = NamedTemporaryFile(delete=False, suffix=".pdf")
        f2.close()

        input_file = f1.name
        output_file = f2.name

        # arguments for ghostscript
        # results in a valid PDF/A-1B document, filesize ~500kb
        command_args = [
            "-dPDFA",
            "-dBATCH",
            "-dNOPAUSE",
            "-sDEVICE=pdfwrite",
            "-sColorConversionStrategy=UseDeviceIndependentColor",
            "-sProcessColorModel=DeviceCMYK",
            "-dPDFSETTINGS=/default",
            "-dPDFACompatibilityPolicy=1",
            "-sOutputFile=" + output_file,
            input_file,
        ]

        try:
            logging.info("=======TANNE MENEE JA AJAA GHOSTIA 2=======");
            ghostscript = [_get_ghostscript_bin()] + command_args
            process = subprocess.Popen(
                ghostscript, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            out, err = process.communicate()

            if err:
                logging.info("=======ERRORIA=======");
                _logger.warning("ghostscript error . Message: %s" % err)

            with open(output_file, "rb") as f3:
                logging.info("=======TANNE MENEE JA AJAA GHOSTIN 3=======");
                pdf = f3.read()

            os.unlink(input_file)
            os.unlink(output_file)

        except (OSError, IOError, ValueError):
            raise

        return pdf
