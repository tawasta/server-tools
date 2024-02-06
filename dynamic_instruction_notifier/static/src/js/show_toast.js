odoo.define('dynamic_instruction_notifier.ActionManager', function (require) {
    "use strict";

    var ActionManager = require('web.ActionManager');
    var session = require('web.session');

    ActionManager.include({
        _executeWindowAction: function (action, options) {
            var result = this._super.apply(this, arguments);
            this._fetchAndShowNotification(action.res_model);
            return result;
        },

        _fetchAndShowNotification: function(res_model) {
            var self = this;
            var paramName = 'instruction_message_' + res_model;

            session.rpc('/web/dataset/call_kw/ir.config_parameter/get_param', {
                model: 'ir.config_parameter',
                method: 'get_param',
                args: [paramName],
                kwargs: {},
            }).then(function(notificationHtml) {
                if (notificationHtml) {
                    // Näytä ilmoitus, jos vastaavaa parametria löytyy ja sillä on arvo
                    self.do_notify(
                        'Notification',
                        notificationHtml,
                        true // Salli HTML-sisältö
                    );
                }
            });
        },
    });
});
