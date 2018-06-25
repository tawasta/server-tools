# -*- coding: utf-8 -*-

import pysftp
import StringIO
from odoo import models


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

                output = StringIO.StringIO()

                output.write(self.get_log_contents())

                # putfo() seems to upload an empty file
                file_name = 'auth_attempts.log'
                tmp_file = '/tmp/%s' % file_name

                fh = open(tmp_file, 'w')
                fh.write(output.getvalue())
                fh.close()
                output.close()

                res = sftp.put(tmp_file, file_name)

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

        contents.append('')  # Generate an extra line break when joining

        return '\n'.join(contents)
