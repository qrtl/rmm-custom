# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    weighing_line_ids = fields.One2many(
        "product.weighing.line",
        "product_tmpl_id",
        string="Weighing Lines",
    )
    weighing_count = fields.Integer(
        compute="_compute_weighing_aggregates",
        store=True,
    )
    total_net_weight = fields.Float(
        digits=(10, 2),
        compute="_compute_weighing_aggregates",
        store=True,
    )
    weighing_confirmed_at = fields.Datetime(
        compute="_compute_weighing_aggregates",
        store=True,
        help="When the most recent weighing line was recorded in Odoo, i.e. the "
        "latest creation timestamp among the lines. This is the time the "
        "external system pushed the result, not the time the weighing itself "
        "took place - for that, see Measured At on the individual lines. The "
        "two differ whenever results are backfilled after an outage.",
    )

    @api.depends(
        "weighing_line_ids",
        "weighing_line_ids.net_weight",
        "weighing_line_ids.create_date",
    )
    def _compute_weighing_aggregates(self):
        for tmpl in self:
            lines = tmpl.weighing_line_ids
            tmpl.weighing_count = len(lines)
            tmpl.total_net_weight = sum(lines.mapped("net_weight"))
            tmpl.weighing_confirmed_at = max(lines.mapped("create_date"), default=False)
