##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2025 Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
    "name": "Base: Access Filters' Domain Selector without Debug Mode",
    "summary": "Allows regular users to access the text-based domain selector",
    "version": "17.0.1.0.1",
    "category": "Server Tools",
    "website": "https://gitlab.com/tawasta/odoo/server-tools",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["web"],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "assets": {
        "web.assets_backend": [
            "base_filter_domain_selector_without_debug_mode/static/src/xml/domain_selector.xml",
        ]
    },
    "data": [],
    "demo": [],
}
