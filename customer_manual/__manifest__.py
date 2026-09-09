##############################################################################
#
#    Author: Futural Oy
#    Copyright 2021- Futural Oy (https://futural.fi)
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
    "name": "Customer Manual",
    "summary": "Customer Manual",
    "version": "17.0.2.0.0",
    "category": "Tools",
    "website": "https://github.com/tawasta/server-tools",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "web",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "https://cdn.ckeditor.com/ckeditor5/36.0.1/classic/ckeditor.js",
            "customer_manual/static/src/js/customer_manual.esm.js",
            "customer_manual/static/src/xml/customer_manual.xml",
            "customer_manual/static/src/scss/customer_manual.scss",
        ],
    },
}
