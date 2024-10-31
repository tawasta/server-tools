##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2024 Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
    "name": "Auth Signup: Separate Firstname and Lastname",
    "summary": "Ask user for their firstname and lastname when registering",
    "version": "17.0.1.0.0",
    "category": "Tools",
    "website": "https://gitlab.com/tawasta/odoo/server-tools",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "auth_signup",
        "partner_firstname",
    ],
    "data": ["views/auth_signup_login_templates.xml"],
    "assets": {
        "web.assets_frontend": [
            "auth_signup_partner_firstname/static/src/js/signup.esm.js",
        ],
    },
}
