# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ValuationStatus(models.Model):
    _name = "valuation.status"
    _description = "Valuation Status"

    name = fields.Char()
