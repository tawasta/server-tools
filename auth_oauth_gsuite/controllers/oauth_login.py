from werkzeug.urls import url_encode
from odoo.addons.auth_oauth.controllers.main import OAuthLogin


class OAuthLoginGsuite(OAuthLogin):

    def list_providers(self):
        res = super(OAuthLoginGsuite, self).list_providers()

        for provider in res:
            if provider.get("hd"):
                params = dict(
                    hd=provider.get("hd"),
                )

                provider["auth_link"] = "%s&%s" % (
                    provider["auth_link"], url_encode(params))

        return res
