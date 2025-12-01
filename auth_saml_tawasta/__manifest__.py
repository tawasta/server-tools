##############################################################################
#
#    Author: Futural Oy
#    Copyright 2025- Futural Oy (https://futural.fi)
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

{
    "name": "Futural SAML",
    "version": "17.0.1.0.0",
    "category": "Tools",
    "author": "Futural Oy",
    "website": "https://gitlab.com/tawasta/odoo/server-tools",
    "license": "AGPL-3",
    "depends": ["base_setup", "auth_saml", "partner_firstname"],
    "external_dependencies": {},
    "demo": [],
    "data": [
        "security/ir.model.access.csv",
        "views/auth_saml.xml",
        "views/auth_saml_token.xml",
        "data/auth_saml_provider.xml",
        "data/auth_saml_attribute_mapping.xml",
        "data/auth_saml_attribute_entity.xml",
        ],
    "installable": True,
    "auto_install": False
}
