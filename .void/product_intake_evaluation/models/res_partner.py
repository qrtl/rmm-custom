# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_intake_evaluation_partner = fields.Boolean(
        default=False,
        copy=False,
    )
    branch_id = fields.Many2one("res.partner")
