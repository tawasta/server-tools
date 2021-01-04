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
    ghostscript_bin = find_in_path('ghostscript')
    if ghostscript_bin is None:
        raise IOError
    return ghostscript_bin


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    report_type = fields.Selection(
        selection_add=[("qweb-pdfa", "PDFA")])

    # @api.model
    # def get_from_report_name(self, report_type):
    #     return self.search(
    #         [("report_type", "=", report_type)])

    @api.multi
    def render_qweb_pdf(self, res_ids=None, data=None):
        if not self.env.context.get('res_ids'):
            pdf = super(
                IrActionsReport, self.with_context(res_ids=res_ids)
            ).render_qweb_pdf(res_ids=res_ids, data=data)

            processed_pdf = self._run_ghostscript(pdf[0])
            return processed_pdf, 'pdf'
        return super(IrActionsReport, self).render_qweb_pdf(res_ids=res_ids, data=data)

    # Runs ghostscript to convert pdf into pdf/a
    def _run_ghostscript(self, pdf):

        with NamedTemporaryFile(delete=False, suffix='.pdf') as f1:
            f1.write(pdf)

        f2 = NamedTemporaryFile(delete=False, suffix='.pdf')
        f2.close()

        input_file = f1.name
        output_file = f2.name

        print(input_file)
        command_args = [
            '-dNOSAFER',
            '-dPDFA',
            '-dBATCH',
            '-dNOPAUSE',
            '-sDEVICE=pdfwrite',
            '-sColorConversionStrategy=UseDeviceIndependentColor',
            '-dPDFACompatibilityPolicy=1',
            '-sOutputFile=' + output_file, input_file]

        try:
            ghostscript = [_get_ghostscript_bin()] + command_args
            print(ghostscript)
            process = subprocess.Popen(ghostscript, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            out, err = process.communicate()

            if err:
                _logger.warning('ghostscript failed . Message: %s' % err)

            with open(output_file, 'rb') as f3:
                pdf = f3.read()

            os.unlink(input_file)
            os.unlink(output_file)

        except (OSError, IOError, ValueError):
            raise

        return pdf
