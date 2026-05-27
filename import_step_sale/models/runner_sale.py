from odoo import models


class RunnerSale(models.AbstractModel):
    _name = "generic.import.runner.sale"
    _inherit = "generic.import.runner.base"
    _description = "Import Runner: Sale Orders and Sale Order Lines"

    def run(self, row_index, row, lines_by_model, state):
        state = dict(state or {})

        sale_order = self._get_or_create_from_lines(
            "sale.order",
            lines_by_model,
            row_index,
            row,
            state=state,
        )

        if sale_order:
            state = self._set_state_record(
                state,
                "sale_order",
                sale_order,
            )

        sale_order_line = self._get_or_create_from_lines(
            "sale.order.line",
            lines_by_model,
            row_index,
            row,
            state=state,
        )

        if sale_order_line:
            state = self._set_state_record(
                state,
                "sale_order_line",
                sale_order_line,
            )

        return state