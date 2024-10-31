/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SignUpFormAuthSignupPartnerFirstname = publicWidget.Widget.extend(
    {
        selector: ".oe_signup_form",

        events: {
            "change input#helper_firstname": "_onFirstOrLastNameChange",
            "change input#helper_lastname": "_onFirstOrLastNameChange",
        },

        /**
         * Populate the hidden 'name' field as user types in the firstname
         * or lastname helper fields
         *
         */
        _onFirstOrLastNameChange: function () {
            // Check partner_firstname config for which order to use for the names
            const nameOrder = this.$el.data("partner-names-order");

            const $firstNameField = this.$el.find("input#helper_firstname");
            const $lastNameField = this.$el.find("input#helper_lastname");
            const $nameField = this.$el.find("input#name");

            let fullName = "";

            switch (nameOrder) {
                case "last_first":
                    fullName = `${$lastNameField.val()} ${$firstNameField.val()}`;
                    break;
                case "last_first_comma":
                    fullName = `${$lastNameField.val()}, ${$firstNameField.val()}`;
                    break;
                default:
                    fullName = `${$firstNameField.val()} ${$lastNameField.val()}`;
                    break;
            }

            $nameField.val(fullName);
        },
    }
);
