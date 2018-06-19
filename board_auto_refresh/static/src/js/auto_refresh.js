odoo.define('web_auto_refresh.board', function (require) {
    "use strict";

    var refresh_page = function(view) {
        setInterval(function() {
            var active_view = view.action_manager.inner_widget.active_view;
            if (typeof(active_view) != 'undefined'){
                try {
                    var controller = view.action_manager.inner_widget.active_view.controller;
                    var action = view.action_manager.inner_widget.action;

                    if (String(action.view_id).match('My Dashboard')) {
                        controller.reload();
                    }
                } catch (e) {
                    alert(e);
                }
            }
        }, 30000);
    }

    openerp.web.WebClient.include({
        start: function() {
            this._super();
            refresh_page(this);
        },

    });
});
