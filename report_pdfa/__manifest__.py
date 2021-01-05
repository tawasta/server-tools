##############################################################################
#
#    Author: Avoin.Systems & Oy Tawasta OS Technologies Ltd.
#    Copyright 2018 Avoin.Systems & Oy Tawasta OS Technologies Ltd.
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
    'name': 'Report - PDF-A',
    'summary': 'Converts QWeb PDF into PDF-A using ghostscript',
    'version': '12.0.1.0.0',
    'category': 'Reporting',
    'website': 'https://github.com/Tawasta/server-tools',
    'author': 'Tawasta',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'external_dependencies': {
        'bin': [
            'ghostscript',
        ],
    },
    'depends': [
        'base',
    ],
    'data': [
        'views/ir_actions_views.xml',
    ],
}
