# -*- coding: utf-8 -*-

# 1. Standard library imports:
import requests
from urllib2 import HTTPError

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class MattermostHook(models.Model):

    # 1. Private attributes
    _name = 'mattermost.hook'

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
        'res.company',
        string='Company',
        help='Company who owns the hook',
    )
    res_model = fields.Many2one(
        'ir.model',
        string='Model',
        help='Which model this hook is related to',
        required=True,
    )
    function = fields.Char(
        string='Method',
        help='Name of the method to be called',
        required=True,
    )
    hook = fields.Char(
        string='Hook key',
        help='The hook generated key',
    )
    channel = fields.Char(
        string='Channel',
        help='Channel the message is posted to',
    )
    username = fields.Char(
        string='Username',
        help='Username who posts the message to Mattermost',
    )
    icon_url = fields.Char(
        string='Icon URL',
        help='Icon url to be used for posting the message',
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def _get_hook_url(self):
        return '{}/hooks/{}'.format(self.mattermost_url, self.hook)

    @api.multi
    def post_mattermost(self, message, verify=True):
        """
        Method to post a message to the hook

        @param message: translated message
        @param channel: channel name
        @param username: username to be posted as
        @param icon_url: URL of an icon to be used
        @param verify: Boolean, is the certificate verified
        @return: None
        @raise ValidationError: Raises exception if no message
        """
        self.ensure_one()
        hook_url = self._get_hook_url()
        if not message.strip():
            raise ValidationError(_('Message can\'t be empty!'))
        payload = {
            'text': message,
        }
        if self.channel:
            payload['channel'] = self.channel
        if self.username:
            payload['username'] = self.username
        if self.icon_url:
            payload['icon_url'] = self.icon_url
        res = requests.post(hook_url, json=payload, verify=verify)
        if res.status_code != 200:
            raise HTTPError(res.text)

    # 8. Business methods
