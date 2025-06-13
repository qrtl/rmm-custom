# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ValuationStatus(models.Model):
    _name = "valuation.status"
    _description = "Valuation Status"
    _order = "sequence, name"

    sequence = fields.Integer()
    name = fields.Char()
