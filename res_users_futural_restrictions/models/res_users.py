from odoo import api, models
from odoo.exceptions import AccessError


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.constrains("login", "groups_id")
    def _check_system_admin_group(self):
        for user in self:
            if user.has_group("base.group_system") and not (
                "@tawasta.fi" in user.login
                or "@futural.fi" in user.login
                or user.login == "tawadmin"
            ):
                raise AccessError(
                    "Assigning Admin system rights to user {} is not possible.".format(
                        user.login
                    )
                )

    @api.model
    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        for record in self:
            if not (
                "@tawasta.fi" in self.env.user.login
                or "@futural.fi" in self.env.user.login
                or self.env.user.login == "tawadmin"
            ) and ("@tawasta.fi" in record.login or "@futural.fi" in record.login):
                raise AccessError("You cannot modify these users.")
        return res
