from odoo import fields, models, _
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    portal_user_signup_origin_url = fields.Char(
        string="Portal User Signup Origin URL",
        help="Website URL from which user initiated signup (e.g. specific product "
        "page). Can be used to redirect freshly created portal user account back to same "
        "page after clicking the signup link in email.",
    )

    def _compute_signup_url(self):
        # Append a sanitized "&redirect=<custom url>" to the end of the URL

        super()._compute_signup_url()

        result = self._get_signup_url_for_action()

        for partner in self:
            if partner.portal_user_signup_origin_url:
                default_signup_url = result.get(partner.id, False)

                url_parts = list(urlparse(default_signup_url))

                # Extract the query parameters
                query = parse_qs(url_parts[4])

                # Append the new parameter to the end
                query["redirect"] = partner.portal_user_signup_origin_url

                # Reconstruct the query string
                url_parts[4] = urlencode(query, doseq=True)

                # Rebuild as string with the new parameter now included
                partner.signup_url = urlunparse(url_parts)
