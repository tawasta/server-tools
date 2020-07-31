import os
import requests
from odoo import models, api


class Module(models.Model):
    _inherit = 'ir.module.module'

    @api.model
    def boot_upgrade(self):
        modules_to_upgrade = self._get_modules_with_changed_checksum()
        if len(modules_to_upgrade) > 0:
            super(Module, self).upgrade_changed_checksum(self)
            if (
                'MATTERMOST_ACCES_TOKEN' in os.environ
                and 'MATTERMOST_URL' in os.environ
            ):
                mattermost_access_token = os.environ['MATTERMOST_ACCESS_TOKEN']
                mattermost_url = os.environ['MATTERMOST_URL']
                url = "{}/{}".format(
                    mattermost_url,
                    mattermost_access_token
                )
                data = "{}{}{}{}".format(
                    '{"text":',
                    '"Modules updated: ',
                    str(modules_to_upgrade),
                    '"}',
                )
                requests.post(
                    url,
                    data=data,
                    headers={
                        "content-type": "applicaton/json"
                    }
                )
