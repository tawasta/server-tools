# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):

# 4. Imports from Odoo modules:
from odoo import http
from odoo.addons.auth_oauth.controllers.main import OAuthLogin

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class OAuthLoginHidden(OAuthLogin):

    @http.route()
    def web_login(self, *args, **kw):
        res = super(OAuthLoginHidden, self).web_login(*args, **kw)

        # Remove hidden providers, unless a GET parameter is given
        if res.qcontext.get('providers', False):
            for provider in res.qcontext['providers']:
                key = kw.get('key', False)
                hidden = provider.get('hidden', False)

                if hidden and key != provider.get('hidden_key'):
                    res.qcontext['providers'].remove(provider)

        return res
