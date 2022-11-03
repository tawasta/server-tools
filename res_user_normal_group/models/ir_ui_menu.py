from odoo import models


class IrUiMenu(models.Model):

    _inherit = "ir.ui.menu"

    def add_normal_user_to_menu(self):
        """Removed Internal User and adds Normal User to menus, which
        have Internal User in their groups."""
        menus = self.search([])
        internal = self.env.ref("base.group_user")
        normal_user = self.env.ref("res_user_normal_group.group_normal_user")

        for menu in menus:
            if internal.id in menu.groups_id.ids:
                menu.groups_id -= internal
                menu.groups_id |= normal_user
            elif not menu.groups_id.ids:
                menu.groups_id |= normal_user
