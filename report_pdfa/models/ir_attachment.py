import base64
import logging
import os
import subprocess
from tempfile import NamedTemporaryFile

from odoo import api, models
from odoo.tools.misc import find_in_path


_logger = logging.getLogger(__name__)


# Check the presence of Ghostscript and return its version at Odoo start-up
def _get_ghostscript_bin():
    ghostscript_bin = find_in_path('ghostscript')
    if ghostscript_bin is None:
        raise IOError
    return ghostscript_bin


ghostscript_state = 'install'
try:
    process = subprocess.Popen(
        [_get_ghostscript_bin(), '--version'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

except (OSError, IOError):
    _logger.info('You need Ghostscript to convert pdfs.')


class IrAttachment(models.Model):

    _inherit = 'ir.attachment'

    @api.model
    def create(self, values):
        _logger.warning('Create function called')
        if 'mimetype' not in values:
            values['mimetype'] = self._compute_mimetype(values)
        if values.get('mimetype') == 'application/pdf' and values.get(
                'datas'):
            try:
                values['datas'] = self._run_ghostscript(values['datas'])
            except (OSError, IOError, ValueError):
                _logger.warning('You need Ghostscript to compress pdfs.')

        return super(IrAttachment, self).create(values)

    @api.multi
    def write(self, values):
        if 'mimetype' not in values:
            values['mimetype'] = self._compute_mimetype(values)
        if values.get('mimetype') == 'application/pdf' and values.get(
                'datas'):
            try:
                values['datas'] = self._run_ghostscript(values['datas'])
            except (OSError, IOError, ValueError):
                _logger.warning('You need Ghostscript to compress pdfs.')

        return super(IrAttachment, self).write(values)

    @api.model
    def _run_ghostscript(self, pdf):

        command_args = []

        with NamedTemporaryFile(delete=False, suffix='.pdf') as f1:
            f1.write(base64.decodestring(pdf))

        f2 = NamedTemporaryFile(delete=False, suffix='.pdf')
        f2.close()

        input_file = f1.name
        output_file = f2.name

        local_command_args = [
            'dPDFA',
            'dBATCH',
            'dNOPAUSE',
            '-sColorConversionStrategy=UseDeviceIndependentColor',
            '-sDEVICE=pdfwrite',
            '-dPDFACompatibilityPolicy=1',
            '-sOutputFile=' + output_file, input_file]

        # local_command_args = [
        #         '-dPDFA=2',
        #         '-dProcessColorModel=/DeviceRGB',
        #         '-dColorConversionStrategy=/RGB',
        #         '-dEmbedAllFonts=true',
        #         '-dMaxSubsetPct=100',
        #         '-dSubsetFonts=true',
        #         '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
        #         '-dNOPAUSE', '-dQUIET', '-dBATCH', '-dNOOUTERSAVE',
        #         '-sOutputFile=' + output_file, input_file]

        try:
            ghostscript = [_get_ghostscript_bin()] + command_args + \
                local_command_args
            process = subprocess.Popen(ghostscript, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            out, err = process.communicate()

            if err:
                _logger.info('ghostscript failed . Message: %s' % err)

            with open(output_file, 'rb') as f3:
                pdf = base64.encodestring(f3.read())

            os.unlink(input_file)
            os.unlink(output_file)

        except (OSError, IOError, ValueError):
            raise

        return pdf
