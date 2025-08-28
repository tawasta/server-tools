import logging

from odoo import _
from odoo.http import request

from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.web.controllers.home import SIGN_UP_REQUEST_PARAMS

_logger = logging.getLogger(__name__)


class AuthSignupParentCompanySelection(AuthSignupHome):
    def _get_allowed_parent_ids(self):
        # Fetch the partners that are allowed to be set as parent when signing up
        partner_obj = request.env["res.partner"]

        return partner_obj.sudo().search(
            [
                ("is_company", "=", True),
                ("industry_id.allows_parent_selection_in_user_signup", "=", True),
            ],
            order="name ASC",
        )

    def _get_partner_id_help_text(self):
        # Fetch help text shown below selection. TODO make configurable in UI if this
        # module gets more use
        return _("If you are a member, select the organization here.")

    def _prepare_signup_values(self, qcontext):
        # Extract the parent ID from submitted form
        values = super()._prepare_signup_values(qcontext)

        if qcontext.get("parent_id", False):
            values["parent_id"] = int(qcontext.get("parent_id"))

        return values

    def get_auth_signup_qcontext(self):
        # Whitelist the new field so that it can be extracted from submitted form
        SIGN_UP_REQUEST_PARAMS.update({"parent_id"})

        qcontext = super().get_auth_signup_qcontext()

        # Extra data for the signup form view
        qcontext["partner_id_help_text"] = self._get_partner_id_help_text()
        qcontext["allowed_parent_ids"] = self._get_allowed_parent_ids()

        return qcontext
