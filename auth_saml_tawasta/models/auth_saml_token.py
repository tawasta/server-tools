# Copyright (C) 2010-2016 XCG Consulting <http://odoo.consulting>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AuthSamlToken(models.Model):
    """Stores information about logged in users"""

    _name = "auth_saml.token"
    _rec_name = "user_id"
    _description = "SAML Token"

    saml_provider_id = fields.Many2one(
        "auth.saml.provider",
        string="SAML Provider that issued the token",
        required=True,
    )
    user_id = fields.Many2one(
        "res.users",
        string="User",
        required=True,
        # we want the token to be destroyed if the corresponding res.users
        # is deleted
        ondelete="cascade",
        index=True,
    )
    saml_access_token = fields.Char(
        "Current SAML token for this user",
        required=False,
        help="The current SAML token in use",
    )
    saml_name_id = fields.Char(
        string="Session name ID value encoded",
        help="The current SAML name ID in use",
    )
