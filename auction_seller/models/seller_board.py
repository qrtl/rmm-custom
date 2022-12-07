# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SellerBoard(models.Model):
    _name = "seller.board"

    name = fields.Char()
    state = fields.Selection(
        [("product", "Product"), ("item", "Item"), ("order", "Order")]
    )
