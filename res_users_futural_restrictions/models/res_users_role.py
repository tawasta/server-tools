from odoo import api, models
from odoo.exceptions import AccessError


class ResUsersRole(models.Model):
    _inherit = "res.users.role"

    @api.model
    def write(self, vals):
        res = super().write(vals)
        for role in self:
            for user in role.user_ids:
                if not (
                    "@tawasta.fi" in self.env.user.login
                    or "@futural.fi" in self.env.user.login
                    or self.env.user.login == "tawadmin"
                ) and ("@tawasta.fi" in user.login or "@futural.fi" in user.login):
                    raise AccessError("You cannot modify these users.")
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
        return res
