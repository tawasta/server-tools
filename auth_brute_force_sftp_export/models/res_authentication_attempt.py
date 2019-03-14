# -*- coding: utf-8 -*-

import logging
from datetime import date, timedelta
from odoo import models

_logger = logging.getLogger(__name__)

try:
    import pysftp
    import StringIO
except (ImportError, IOError) as err:
    _logger.debug(err)


class ResAuthenticationAttempt(models.Model):
    _inherit = 'res.authentication.attempt'

    def action_cron_export_to_ftp(self):

        IrConfigParameter = self.env['ir.config_parameter'].sudo()

        username = IrConfigParameter.get_param(
            'auth_brute_force_ftp_export.username', ''
        )

        password = IrConfigParameter.get_param(
            'auth_brute_force_ftp_export.password', ''
        )

        host = IrConfigParameter.get_param(
            'auth_brute_force_ftp_export.host', ''
        )

        with pysftp.Connection(
                host=host,
                username=username,
                password=password,
        ) as sftp:
                yesterday_date = date.today() - timedelta(1)
                yesterday = yesterday_date.strftime('%Y-%m-%d')
                yesterday_start = '{0} 00:00:00'.format(yesterday)
                yesterday_end = '{0} 23:59:59'.format(yesterday)

                output = StringIO.StringIO()

                log_contents = self.get_log_contents(
                    yesterday_start,
                    yesterday_end,
                )
                output.write(log_contents)

                # putfo() seems to upload an empty file
                file_name = 'auth_attempts_{0}.log'.format(yesterday)
                tmp_file = '/tmp/%s' % file_name

                fh = open(tmp_file, 'w')
                fh.write(output.getvalue().encode('utf-8'))
                fh.close()
                output.close()

                sftp.put(tmp_file, file_name)

    def get_log_contents(self, date_from=False, date_to=False):
        domain = list()

        if date_from:
            domain.append(('create_date', '>=', date_from))

        if date_to:
            domain.append(('create_date', '<=', date_to))

        contents = list()

        for attempt in self.search(domain):
            line = '%s login from %s as %s: %s' % \
                   (
                       attempt.create_date,
                       attempt.remote,
                       attempt.login,
                       attempt.result,
                   )
            contents.append(line)

        # Reverse the list
        contents = contents[::-1]
        contents.append('')  # Generate an extra line break when joining

        return '\n'.join(contents)
