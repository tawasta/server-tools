odoo.define("res_user_change_company_helper.SwitchCompanyMenu", function (require) {
    "use strict";

    var session = require("web.session");
    var SwitchCompanyMenu = require("web.SwitchCompanyMenu");

    SwitchCompanyMenu.include({
        _onSwitchCompanyClick: function (ev) {
            var $res = this._super.apply(this, arguments);

            var chosen_company_id = $(ev.currentTarget).parent().data("company-id");

            this._rpc({
                method: "write",
                model: "res.users",
                args: [
                    [session.uid],
                    {
                        company_id: chosen_company_id,
                    },
                ],
            });

            return $res;
        },
    });
});
