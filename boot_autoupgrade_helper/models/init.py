import os
import requests
from odoo import models, api


class Module(models.Model):
    _inherit = 'ir.module.module'

    @api.model
    def boot_upgrade(self):
        modules_to_upgrade = self._get_modules_with_changed_checksum()
        if len(modules_to_upgrade) > 1:
            super(Module, self).upgrade_changed_checksum(self)

            if 'GITLAB_WEBHOOK_PASSWORD' in os.environ:
                mattermost_access_token = os.environ['GITLAB_WEBHOOK_PASSWORD']
                url = "https://matters.intra.fi/hooks/{}"\
                    .format(mattermost_access_token)
                data = {'text': 'Modules udpated: {}'
                        .format(str(modules_to_upgrade))}
                requests.post(url, data=data)
