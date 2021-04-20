import logging
from odoo import api, models, _
from odoo.exceptions import AccessDenied
_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _auth_oauth_validate(self, provider, access_token):
        res = super(ResUsers, self)._auth_oauth_validate(
            provider=provider,
            access_token=access_token,
        )

        oauth_provider = self.env["auth.oauth.provider"].browse(provider)

        if oauth_provider.hd and not res.get("hd") == oauth_provider.hd:
            msg = _("'%s' tried to login from outside of the domain"
                    % res.get("email"))
            _logger.warning(msg)
            raise AccessDenied()

        return res
