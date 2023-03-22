##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2019- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, models


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class AuthSamlAttributeEntity(models.Model):

    # 1. Private attributes
    _name = "auth.saml.attribute.entity"
    _description = "Entity attributes for SAML provider"

    # 2. Fields declaration
    provider_id = fields.Many2one(
        comodel_name="auth.saml.provider",
        index=True,
        required=True,
    )
    name_format = fields.Char(
        string="Name format",
        help="What's the attributes name format",
        default="urn:oasis:names:tc:SAML:2.0:attrname-format:uri",
        required=True,
    )
    name = fields.Char(
        string="Name",
        help="What's the attributes name",
        required=True,
    )
    friendly_name = fields.Char(
        string="Friendly name",
        help="What's the attributes friendly name",
    )
    value = fields.Char(
        string="Attribute value(s)",
        help="What's the attributes values (separate multiple with comma)",
        required=True,
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def get_entity_attributes_metadata(self):
        """ Return list for metadata from defined attributes """
        result = []
        for rec in self:
            vals = {
                "name_format": rec.name_format,
                "name": rec.name,
                "values": [val.strip() for val in rec.value.split(",")]
            }
            if rec.friendly_name:
                vals["friendly_name"] = rec.friendly_name
            result.append(vals)
        return result

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
