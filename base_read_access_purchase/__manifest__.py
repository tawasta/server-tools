##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2018 Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
    'name': 'Read Access Group for Purchases',
    'summary': 'Adds a new group that can read purchase-related model data',
    'version': '12.0.1.0.0',
    'category': 'Extra Rights',
    'website': 'https://github.com/Tawasta/server-tools',
    'author': 'Oy Tawasta Technologies Ltd.',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'depends': [
        'purchase',
        'stock',
    ],
    'data': [
        'data/res_groups.xml',
        'data/ir_ui_menu.xml',
        'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/res_partner.xml',
    ],
    'demo': [
    ],
}
