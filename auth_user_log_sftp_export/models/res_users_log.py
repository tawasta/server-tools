import logging
from datetime import date, timedelta
from odoo import models

_logger = logging.getLogger(__name__)

try:
    import pysftp
    import io
except (ImportError, IOError) as err:
    _logger.debug(err)


class ResUsersLog(models.Model):
    _inherit = "res.users.log"

    def action_cron_export_to_ftp(self):

        IrConfigParameter = self.env["ir.config_parameter"].sudo()

        username = IrConfigParameter.get_param("auth_user_log_sftp_export.username", "")
        password = IrConfigParameter.get_param("auth_user_log_sftp_export.password", "")
        host = IrConfigParameter.get_param("auth_user_log_sftp_export.host", "")

        with pysftp.Connection(host=host, username=username, password=password) as sftp:
            yesterday_date = date.today() - timedelta(1)
            yesterday = yesterday_date.strftime("%Y-%m-%d")
            yesterday_start = "{0} 00:00:00".format(yesterday)
            yesterday_end = "{0} 23:59:59".format(yesterday)

            log_contents = self.get_log_contents(yesterday_start, yesterday_end)

            file_name = "auth_attempts_{0}.log".format(yesterday)
            _logger.debug("Auth log contents: {}".format(log_contents))
            _logger.debug("Moving auth log {} to {}".format(file_name, host))

            sftp.putfo(io.StringIO(log_contents), file_name)

    def get_log_contents(self, date_from=False, date_to=False):
        domain = list()

        if date_from:
            domain.append(("create_date", ">=", date_from))

        if date_to:
            domain.append(("create_date", "<=", date_to))

        contents = list()

        for attempt in self.search(domain):
            line = "%s login as %s" % (attempt.create_date, attempt.create_uid.login)
            contents.append(line)

        # Reverse the list
        contents = contents[::-1]
        contents.append("")  # Generate an extra line break when joining

        return "\n".join(contents)
