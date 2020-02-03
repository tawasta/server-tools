from odoo import models, api, fields
import datetime

class Module(models.Model):
    _inherit = 'ir.module.module'
    last_boot_upgrade = fields.Datetime.context_timestamp(self, timestamp=datetime.datetime.now())

    @api.model
    def boot_upgrade(self):
        if last_boot_update < datetime.datetime.now() - datetime.timedelta(seconds=10):
            last_boot_upgrade = datetime.datetime.now()
            return super(Module, self).upgrade_changed_checksum(self)
