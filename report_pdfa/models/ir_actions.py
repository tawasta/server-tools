# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ReportAction(models.Model):
    _inherit = "ir.actions.report"

    report_type = fields.Selection(selection_add=[("qweb-pdfa", "PDFA")])

    @api.multi
    def postprocess_pdf_report(self, record, buffer):
        '''Hook to handle post processing during the pdf report generation.
        The basic behavior consists to create a new attachment containing the pdf
        base64 encoded.
        :param record_id: The record that will own the attachment.
        :param pdf_content: The optional name content of the file to avoid reading both times.
        :return: A modified buffer if the previous one has been modified, None otherwise.
        '''
        attachment_name = safe_eval(self.attachment, {'object': record, 'time': time})
        if not attachment_name:
            return None
        attachment_vals = {
            'name': attachment_name,
            'datas': base64.encodestring(buffer.getvalue()),
            'datas_fname': attachment_name,
            'res_model': self.model,
            'res_id': record.id,
        }
        try:
            self.env['ir.attachment'].create(attachment_vals)
        except AccessError:
            _logger.info("Cannot save PDF report %r as attachment", attachment_vals['name'])
        else:
            _logger.info('The PDF document %s is now saved in the database', attachment_vals['name'])
        return buffer

