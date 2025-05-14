# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class DeliveryCarrierBoard(models.Model):
    _name = "delivery.carrier.board"
    _description = "Delivery Carrier Board"

    name = fields.Char()
    board_type = fields.Selection([("product", "Products")])
