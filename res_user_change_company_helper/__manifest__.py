##############################################################################
#
#    Author: Futural Oy
#    Copyright 2023 Futural Oy (https://futural.fi)
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
    "name": "Directly change user's Default company from dropdown menu",
    "summary": "Company dropdown also changes company_id value for user",
    "version": "17.0.1.0.0",
    "category": "Technical",
    "website": "https://github.com/tawasta/server-tools",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "web",
    ],
    "assets": {
        "web.assets_backend": [
            "res_user_change_company_helper/static/src/js/change_company.esm.js"
        ],
    },
}
