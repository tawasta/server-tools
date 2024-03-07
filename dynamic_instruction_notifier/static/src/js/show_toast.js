odoo.define("dynamic_instruction_notifier.ActionManager", function(require) {
    "use strict";

    var ActionManager = require("web.ActionManager");
    var session = require("web.session");

    ActionManager.include({
        _executeWindowAction: function(action) {
            var result = this._super.apply(this, arguments);
            this._fetchAndShowNotification(action.res_model);
            return result;
        },

        _fetchAndShowNotification: function(res_model) {
            var self = this;
            session.rpc("/get_instruction_message", {model_name: res_model})
                .then(function(notificationHtml) {
                    if (notificationHtml) {
                        // Näytä ilmoitus, jos ohjeviesti löytyy
                        self.do_notify("Notification", notificationHtml, true); // Salli HTML-sisältö
                    }
                });
        },
    });
});
