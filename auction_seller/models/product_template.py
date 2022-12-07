# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    seller_id = fields.Many2one(
        "res.partner", domain="[('is_seller_partner','=',True)]"
    )
    event_ids = fields.Many2many("event.event")
