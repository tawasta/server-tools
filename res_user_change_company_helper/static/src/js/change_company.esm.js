/** @odoo-module **/
import {SwitchCompanyItem} from "@web/webclient/switch_company_menu/switch_company_menu";
import {patch} from "@web/core/utils/patch";
import {session} from "@web/session";
import {useService} from "@web/core/utils/hooks";

patch(SwitchCompanyItem.prototype, {
    setup() {
        this.rpc = useService("rpc");
        super.setup();
    },

    /**
     *  Make an extra RPC call to change the company_id field value
     *  when user changes company in the UI
     *
     */
    logIntoCompany() {
        const companyId = this.props.company.id;
        const userId = session.uid;

        // Currently done with a simple RPC call, in 17
        // there might be a nicer more "owl-ish" way to do this already
        this.rpc("/web/dataset/call_kw/res.users/write/", {
            method: "write",
            model: "res.users",
            args: [
                [userId],
                {
                    company_id: companyId,
                },
            ],
            kwargs: {},
        });

        super.logIntoCompany(...arguments);
    },
});
