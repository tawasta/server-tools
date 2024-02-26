import json

from werkzeug.urls import url_encode

from odoo.http import request

from odoo.addons.auth_oauth.controllers.main import OAuthLogin


class OAuthLoginGsuite(OAuthLogin):
    def list_providers(self):
        res = super(OAuthLoginGsuite, self).list_providers()

        # Punycode URLs (xn--typyt-kra6jb.fi -> työpöytä.fi) require
        # base_url + web.base.url.freeze (url_root doesn't work)
        base_url = (
            request.env["ir.config_parameter"].sudo().get_param("web.base.url", "")
        )
        for provider in res:
            return_url = base_url + "/auth_oauth/signin"
            state = self.get_state(provider)
            params = dict(
                response_type="token",
                client_id=provider["client_id"],
                redirect_uri=return_url,
                scope=provider["scope"],
                state=json.dumps(state),
            )
            if provider.get("hd"):
                params.update(hd=provider.get("hd"))

            provider["auth_link"] = "{}?{}".format(
                provider["auth_endpoint"], url_encode(params)
            )
        return res
