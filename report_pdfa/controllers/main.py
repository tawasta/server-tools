from odoo.addons.web.controllers import main as report
from odoo.http import content_disposition, route, request
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

import json
import time
import werkzeug
import logging

_logger = logging.getLogger(__name__)

class ReportController(report.ReportController):
    @route()
    def report_routes(self, reportname, docids=None, converter=None, **data):

        _logger.warning('test')

        return super(ReportController, self).report_routes(
            reportname, docids, converter, **data
        )
