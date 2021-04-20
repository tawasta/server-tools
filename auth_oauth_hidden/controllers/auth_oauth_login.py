from odoo import http
from odoo.addons.auth_oauth.controllers.main import OAuthLogin


class OAuthLoginHidden(OAuthLogin):

    @http.route()
    def web_login(self, *args, **kw):
        res = super(OAuthLoginHidden, self).web_login(*args, **kw)

        # Remove hidden providers, unless a GET parameter is given
        if res.qcontext.get("providers"):
            key = kw.get("key", False)
            providers = []

            for provider in res.qcontext["providers"]:
                hidden = provider.get("hidden", False)

                if hidden and key != provider.get("hidden_key"):
                    continue

                providers.append(provider)

            res.qcontext["providers"] = providers

        return res

    def get_auth_signup_qcontext(self):
        res = super(OAuthLoginHidden, self).get_auth_signup_qcontext()
        providers = []

        # Don"t show hidden providers in signup
        for provider in res.get("providers"):
            if provider.get("hidden"):
                continue

            providers.append(provider)

        res["providers"] = providers

        return res
