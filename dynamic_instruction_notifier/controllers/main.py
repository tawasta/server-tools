from odoo import http
from odoo.http import request


class PortalNotificationController(http.Controller):
    @http.route("/get_portal_notification", type="json", auth="user", website=True)
    def get_portal_notification(self, xmlid):
        # Etsi oikea ir.ui.view käyttäen xmlid:tä
        view = request.env["ir.ui.view"].sudo().search([("key", "=", xmlid)], limit=1)

        # Jos vastaava näkymä löytyy, etsi siihen liittyvä ohjeviesti
        if view:
            instruction_message = (
                request.env["instruction.message"]
                .sudo()
                .search([("view_id", "=", view.id)], limit=1)
            )

            # Jos ohjeviesti löytyy, palauta sen HTML-sisältö
            if instruction_message:
                return instruction_message.html_content

        # Jos mitään ei löydy, palauta tyhjä merkkijono tai oletusviesti
        return ""

    @http.route("/get_instruction_message", type="json", auth="user")
    def get_instruction_message(self, model_name):
        InstructionMessage = request.env["instruction.message"].sudo()
        instruction_message = InstructionMessage.search(
            [("model_id.model", "=", model_name)], limit=1
        )

        if instruction_message:
            return instruction_message.html_content

        return ""
