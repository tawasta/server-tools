odoo.define("board_auto_refresh.auto_refresh", function (require) {
    "use strict";

    var WebClient = require("web.WebClient");

    var refresh_page = function (view) {
        setInterval(function () {
            var controller_id = view.action_manager.controllerStack[0];
            var controller = view.action_manager.controllers[controller_id];
            var action = view.action_manager.actions[controller.actionID];

            if (typeof action !== "undefined") {
                try {
                    // TODO: This is very inefficient way to do the refresh
                    if (
                        action.view_id &&
                        String(action.view_id[1]).match("My Dashboard")
                    ) {
                        controller.widget.reload();
                    }
                } catch (e) {
                    alert(e);
                }
            }
        }, 300000);
    };

    WebClient.include({
        start: function () {
            this._super();
            refresh_page(this);
        },
    });
});
