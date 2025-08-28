/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SignUpFormAuthSignupParentCompanySelection =
    publicWidget.Widget.extend({
        selector: ".oe_signup_form",

        /**
         * Enable select2 for the parent partner dropdown
         */
        start: function () {
            this._super();
            this.$target.find("select#parent_id").select2();
        },
    });
