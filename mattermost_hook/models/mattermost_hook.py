import requests

from odoo import _, fields, models
from odoo.exceptions import UserError, ValidationError


class MattermostHook(models.Model):

    _name = "mattermost.hook"
    _description = "Mattermost hooks"

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
        default=lambda self: self.env.company,
        required=True,
    )
    res_model = fields.Many2one(
        "ir.model",
        string="Model",
        help="Which model this hook is related to",
        required=True,
        ondelete="cascade",
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

    def _get_hook_url(self):
        return "{}/hooks/{}".format(self.mattermost_url, self.hook)

    def post_mattermost(
        self, message, channel=False, username=False, icon_url=False, verify=True
    ):
        for record in self:
            msg = "Run mattermost hook '{}' using method '{}'".format(
                record.name, record.function
            )
            record.with_delay(description=msg)._post_mattermost(
                message, channel, username, icon_url, verify
            )

    def _post_mattermost(
        self, message, channel=False, username=False, icon_url=False, verify=True
    ):
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
            raise ValidationError(_("Message can't be empty!"))
        payload = {
            "text": message,
        }

        if not channel:
            channel = self.channel

        if not username:
            username = self.username

        if not icon_url:
            icon_url = self.icon_url

        if channel:
            payload["channel"] = channel
        if username:
            payload["username"] = username
        if icon_url:
            payload["icon_url"] = icon_url
        res = requests.post(hook_url, json=payload, verify=verify)
        if res.status_code != 200:
            raise requests.exceptions.HTTPError(res.text)

    def action_test_hook(self):
        """Test if hook is working"""
        self.ensure_one()
        try:
            test_msg = "It worked, great job. Go nuts!"
            self.post_mattermost(test_msg)
        except Exception:
            msg = "An error occured, most likely cause hook settings are incorrect!"
            raise UserError(msg) from Exception
