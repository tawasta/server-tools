odoo.define("dynamic_instruction_notifier.portal_notifications", function (require) {
    "use strict";

    var ajax = require("web.ajax");
    $(document).ready(function () {
        var xmlid = $("html").data("view-xmlid");

        if (xmlid) {
            ajax.jsonRpc("/get_portal_notification", "call", {xmlid: xmlid}).then(
                function (notificationHtml) {
                    if (notificationHtml) {
                        // eslint-disable-next-line no-undef
                        Swal.fire({
                            position: "top-end",
                            icon: "info",
                            title: "Tärkeä ilmoitus!",
                            html: notificationHtml,
                            showConfirmButton: true,
                            confirmButtonText: "Sulje",
                            timer: 20000,
                            timerProgressBar: true,
                            toast: true,
                            customClass: {
                                popup: "swal2-toast-popup",
                            },
                        });
                    }
                }
            );
        }
    });
});
