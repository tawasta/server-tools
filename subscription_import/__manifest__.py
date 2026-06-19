##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2018 Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
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
    "name": "Upload and Generate Subscriptions",
    "summary": "Upload and Generate Subscriptions",
    "version": "17.0.1.0.0",
    "category": "Specific Industry Applications",
    "website": "https://github.com/tawasta/odoo/subscrion",
    "author": "Futural Oy",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "subscription_oca",
        "contacts",
        "sale_management",
    ],
    "external_dependencies": {"python": ["openpyxl"]},
    "data": [
        "security/ir.model.access.csv",
        "views/subscription_import_template_views.xml",
        "views/menu.xml",
        "wizards/file_upload_wizard_view.xml",
    ],
}
