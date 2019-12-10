from odoo import http
from odoo.addons.auth_oauth.controllers.main import OAuthLogin


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
