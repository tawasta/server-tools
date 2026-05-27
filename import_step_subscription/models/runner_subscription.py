from odoo import models


class RunnerSubscription(models.AbstractModel):
    _name = "generic.import.runner.subscription"
    _inherit = "generic.import.runner.base"
    _description = "Import Runner: Subscriptions and Subscription Lines"

    def run(self, row_index, row, lines_by_model, state):
        state = dict(state or {})

        subscription = self._get_or_create_from_lines(
            "sale.subscription",
            lines_by_model,
            row_index,
            row,
            state=state,
        )

        if subscription:
            state = self._set_state_record(
                state,
                "subscription",
                subscription,
            )

        subscription_line = self._get_or_create_from_lines(
            "sale.subscription.line",
            lines_by_model,
            row_index,
            row,
            state=state,
        )

        if subscription_line:
            state = self._set_state_record(
                state,
                "subscription_line",
                subscription_line,
            )

        return state