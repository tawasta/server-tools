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
    'name': 'Export auth attempt logs to SFTP server',
    'summary': 'Export auth attempt logs to SFTP server',
    'version': '10.0.1.1.1',
    'category': 'Tools',
    'website': 'https://github.com/Tawasta/server-tools',
    'author': 'Oy Tawasta Technologies Ltd',
    'license': 'AGPL-3',
    'application': False,
    'installable': False,
    'external_dependencies': {
        'python': [
            'os',
            'paramiko',
            'pysftp',
            'StringIO',
        ],
        'bin': [],
    },
    'depends': [
        'auth_brute_force',
    ],
    'data': [
        'data/ir_config_parameter.xml',
        'data/ir_cron.xml',
    ],
    'demo': [
    ],
}
