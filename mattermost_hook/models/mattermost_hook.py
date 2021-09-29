##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:
import requests

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class MattermostHook(models.Model):

    # 1. Private attributes
    _name = "mattermost.hook"
    _description = "Mattermost hooks"

    # 2. Fields declaration
    name = fields.Char(
        required=True,
    )
    mattermost_url = fields.Char(
        string="Mattermost URL",
        help="Mattermost URL (without trailing backlash)",
        required=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        help="Company who owns the hook",
    )
    res_model = fields.Many2one(
        "ir.model",
        string="Model",
        help="Which model this hook is related to",
        required=True,
    )
    function = fields.Char(
        string="Method",
        help="Name of the method to be called",
        required=True,
    )
    hook = fields.Char(
        string="Hook key",
        help="The hook generated key",
    )
    channel = fields.Char(
        string="Channel",
        help="Channel the message is posted to",
    )
    username = fields.Char(
        string="Username",
        help="Username who posts the message to Mattermost",
    )
    icon_url = fields.Char(
        string="Icon URL",
        help="Icon url to be used for posting the message",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def _get_hook_url(self):
        return "{}/hooks/{}".format(self.mattermost_url, self.hook)

    @api.multi
    def post_mattermost(self, message, verify=True):
        """
        Method to post a message to the hook

        :param message: translated message
        :param channel: channel name
        :param username: username to be posted as
        :param icon_url: URL of an icon to be used
        :param verify: Boolean, is the certificate verified
        :return: None
        :raise ValidationError: Raises exception if no message
        """
        self.ensure_one()
        hook_url = self._get_hook_url()
        if not message.strip():
            raise ValidationError(_("Message can\'t be empty!"))
        payload = {
            "text": message,
        }
        if self.channel:
            payload["channel"] = self.channel
        if self.username:
            payload["username"] = self.username
        if self.icon_url:
            payload["icon_url"] = self.icon_url
        res = requests.post(hook_url, json=payload, verify=verify)
        if res.status_code != 200:
            raise requests.exceptions.HTTPError(res.text)

    @api.multi
    def action_test_hook(self):
        """ Test if hook is working """
        self.ensure_one()
        try:
            test_msg = "It worked, great job. Go nuts!"
            self.post_mattermost(test_msg)
        except Exception:
            msg = "An error occured, most likely cause hook settings are incorrect!"
            raise UserError(msg)

    # 8. Business methods
