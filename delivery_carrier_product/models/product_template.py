# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    valuation_status_id = fields.Many2one('valuation.status')
    carrier_branch = fields.Char()
    carrier_contact_person = fields.Char()
    tracking_no_1 = fields.Char()
    tracking_no_2 = fields.Char()
    valuation_comment = fields.Text()
