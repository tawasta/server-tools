from odoo import api
from odoo import models
from odoo import fields

PARAM_AUTO_UPDATE_DATE = "module_auto_update_on_boot.last_update_date"


class IrModule(models.Model):
    _inherit = "ir.module.module"

    @api.model
    def upgrade_changed_checksum(self, upgrade_changed_checksum=False):
        # Save the last update date
        self.env["ir.config_parameter"].set_param(
            PARAM_AUTO_UPDATE_DATE, fields.datetime.now().isoformat()
        )

        return super().upgrade_changed_checksum(upgrade_changed_checksum)
