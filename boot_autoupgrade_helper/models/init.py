from odoo import models, api, fields
import datetime


class LastBootUpgradeTimeCompany(models.Model):
    _inherit = 'res.company'
    last_boot_upgrade = fields.Datetime(
        string='Last time all module upgrade happened on boot',
        default=datetime.datetime.now() - datetime.timedelta(hours=1),
        readonly=False
    )


class Module(models.Model):
    _inherit = 'ir.module.module'

    @api.model
    def boot_upgrade(self):
        if self.env.user.company_id.last_boot_upgrade < datetime.datetime.now()\
                - datetime.timedelta(minutes=11):
            self.env.user.company_id.last_boot_upgrade = datetime.datetime.now()
            return super(Module, self).upgrade_changed_checksum(self)
