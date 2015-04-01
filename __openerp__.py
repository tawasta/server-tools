# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2015- Vizucom Oy (http://www.vizucom.com)
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
    'name': 'Mail blacklist',
    'category': 'Tools',
    'version': '0.1',
    'author': 'Vizucom Oy',
    'website': 'http://www.vizucom.com',
    'depends': [
        'mail'
    ],
    'description': """
IR Attachment Extension
===================================
* Allows blacklisting outgoing mail addresses
* TODO: outgoing mail domains
* TODO: incoming mail addresses
* TODO: incoming mail domains

""",
    'data': [
        'view/mail_blacklist_menu.xml',
    ],
}
