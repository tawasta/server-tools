import base64

from odoo import _, http
from odoo.http import request


class CustomerManualController(http.Controller):
    @http.route(
        "/customer_manual/upload_image",
        type="http",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def upload_image(self, upload=None, **kwargs):
        if not request.env.user.has_group("customer_manual.group_customer_manual_edit"):
            return request.make_json_response(
                {
                    "uploaded": 0,
                    "error": {
                        "message": _("You are not allowed to upload images here.")
                    },
                }
            )

        if not upload or not (upload.content_type or "").startswith("image/"):
            return request.make_json_response(
                {
                    "uploaded": 0,
                    "error": {"message": _("Only image files can be uploaded.")},
                }
            )

        attachment = (
            request.env["ir.attachment"]
            .sudo()
            .create(
                {
                    "name": upload.filename,
                    "datas": base64.b64encode(upload.read()),
                    "res_model": "customer.manual.note",
                    "public": True,
                }
            )
        )
        return request.make_json_response(
            {"uploaded": 1, "url": f"/web/image/{attachment.id}"}
        )
