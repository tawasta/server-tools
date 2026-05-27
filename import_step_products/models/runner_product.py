from odoo import models


class RunnerProduct(models.AbstractModel):
    _name = "generic.import.runner.product"
    _inherit = "generic.import.runner.base"
    _description = "Import Runner: Products"

    def run(self, row_index, row, lines_by_model, state):
        state = dict(state or {})

        product_template = self._get_or_create_from_lines(
            "product.template",
            lines_by_model,
            row_index,
            row,
            state=state,
        )

        if not product_template:
            return state

        state = self._set_state_record(
            state,
            "product_template",
            product_template,
        )

        product = product_template.product_variant_id
        if product:
            state = self._set_state_record(
                state,
                "product",
                product,
            )

        return state