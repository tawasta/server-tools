from odoo import fields, models


class ResPartnerIndustry(models.Model):
    _inherit = "res.partner.industry"

    allows_parent_selection_in_user_signup = fields.Boolean(
        string="Selectable in User Signup",
        help="If checked, companies of this industry can be selected as parent "
        "organizations by users when they sign up as portal users.",
    )
