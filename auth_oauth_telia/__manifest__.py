# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Telia Authentication',
    'category': 'Hidden/Tools',
    'description': "",
    'depends': ['base', 'web', 'base_setup', 'auth_signup'],
    'data': [
        'data/auth_oauth_data.xml',
        'views/auth_oauth_views.xml',
        'views/res_users_views.xml',
        #'views/res_config_settings_views.xml',
        'views/auth_oauth_templates.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_frontend': [
            'auth_oauth_telia/static/**/*',
        ],
    },
    'license': 'LGPL-3',
}
