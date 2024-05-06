from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    value = fields.Monetary(
        groups="stock.group_stock_manager,base_read_access_stock.group_readonly"
    )
