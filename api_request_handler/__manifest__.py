##############################################################################
#
#    Author: Futural Oy
#    Copyright 2025 Futural Oy (https://futural.fi)
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
    "name": "API Request Handler",
    "summary": "Base module for handling API/HTTP requests",
    "version": "17.0.1.1.3",
    "category": "Tools",
    "website": "https://github.com/tawasta/server-tools",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "python": ["httpx"],
    "depends": [
        "base",
        "queue_job",
    ],
    "data": [
        "security/model_access.xml",
        "views/api_request_menu.xml",
        "views/api_request_form.xml",
        "views/api_request_search.xml",
        "views/api_request_tree.xml",
    ],
}
