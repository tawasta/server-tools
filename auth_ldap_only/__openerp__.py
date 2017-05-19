# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2015- Oy Tawasta Technologies Ltd. (http://www.tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Authentication via LDAP Only',
    'category': 'Authentication',
    'version': '1.0',
    'author': 'Oy Tawasta Technologies Ltd',
    'website': 'http://www.tawasta.fi',
    'depends': [
        'auth_ldap',
    ],
    'data': [
        'view/res_users_form.xml',
    ],
    'description': 
'''
Auth LDAP Only
--------------

Auth LDAP Only is an extension to [auth\_ldap](https://github.com/OCA/OCB/tree/8.0/addons/auth_ldap)

Disables logins against local passwords in Odoo res_users database.

Features
--------

* Only allows LDAP-authorization (disables local logins)
* Admin is excluded from LDAP-authorization, and can login via local password
'''
}
