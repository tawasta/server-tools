from odoo import models, fields, api, _
from datetime import timedelta


class KsDashboardNinja(models.Model):

    _inherit = "ks_dashboard_ninja.item"

    ks_date_filter_selection = fields.Selection(
        selection_add=[
            ('l_custom_test', 'Next 90 days'),
        ],
        ondelete={"l_custom_test": "set default"},
    )

    ks_date_filter_selection_2 = fields.Selection(
        selection_add=[
            ('l_custom_test', 'Next 90 days'),
        ],
        ondelete={"l_custom_test": "set default"},
    )

    next_90_days_selected = fields.Boolean(default=False)
    next_90_days_selected_2 = fields.Boolean(default=False)


    def ks_convert_into_proper_domain(self, ks_domain, rec, domain=[]):
        if self.ks_date_filter_selection == 'l_custom_test':
            self.ks_date_filter_selection = 'l_custom'

        if self.ks_date_filter_selection_2 == 'l_custom_test':
            self.ks_date_filter_selection_2 = 'l_custom'

        res = super(KsDashboardNinja, self).ks_convert_into_proper_domain(ks_domain, rec, domain)

        if self.ks_date_filter_selection == 'l_custom' and self.next_90_days_selected:
            self.ks_date_filter_selection = 'l_custom_test'
        
        if self.ks_date_filter_selection_2 == 'l_custom' and self.next_90_days_selected_2:
            self.ks_date_filter_selection_2 = 'l_custom_test'

        return res
    

    @api.onchange('ks_date_filter_selection')
    def ks_set_date_filter(self):
        if self.ks_date_filter_selection == "l_custom_test":
            self.ks_date_filter_selection = 'l_custom'
            self.next_90_days_selected = True
        else:
            self.next_90_days_selected = False

        res = super(KsDashboardNinja, self).ks_set_date_filter()

        if self.ks_date_filter_selection == 'l_custom' and self.next_90_days_selected:
            self.ks_item_start_date = fields.Datetime.now()
            ninety_days_from_now = fields.Datetime.now() + timedelta(days=90)
            self.ks_item_end_date = ninety_days_from_now

        return res
    
    
    @api.onchange('ks_date_filter_selection_2')
    def ks_set_date_filter_2(self):
        if self.ks_date_filter_selection_2 == "l_custom_test":
            self.ks_date_filter_selection_2 = 'l_custom'
            self.next_90_days_selected_2 = True
        else:
            self.next_90_days_selected_2 = False

        res = super(KsDashboardNinja, self).ks_set_date_filter_2()

        if self.ks_date_filter_selection_2 == 'l_custom' and self.next_90_days_selected_2:
            self.ks_item_start_date_2 = fields.Datetime.now()
            ninety_days_from_now = fields.Datetime.now() + timedelta(days=90)
            self.ks_item_end_date_2 = ninety_days_from_now

        return res