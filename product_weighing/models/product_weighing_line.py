# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import AccessError


class ProductWeighingLine(models.Model):
    _name = "product.weighing.line"
    _description = "Weighing Line"
    _order = "measured_at desc"

    product_tmpl_id = fields.Many2one(
        "product.template",
        string="Product",
        required=True,
        ondelete="restrict",
        index=True,
    )
    weighing_id = fields.Char(
        string="Weighing ID",
        required=True,
        index=True,
        help="External weighing identifier (e.g. WEIGH-KNG-20260513-0001).",
    )
    measured_at = fields.Datetime(required=True)
    measurer_name = fields.Char(string="Measurer")
    receipt_no = fields.Char(string="Receipt No.")
    gross_weight = fields.Float(
        string="Gross Weight (kg)", digits=(10, 2), required=True
    )
    dust_detail = fields.Char(
        string="Dust Deduction Detail",
        help="Breakdown of deducted items (e.g. 'cage cart x2, cart x1').",
    )
    dust_weight = fields.Float(
        string="Dust Deduction Weight (kg)",
        digits=(10, 2),
        required=True,
    )
    net_weight = fields.Float(string="Net Weight (kg)", digits=(10, 2), required=True)
    image_hash = fields.Text(
        help="SHA-256 of the evidence image(s), comma-separated, for tamper "
        "verification.",
    )

    _sql_constraints = [
        (
            "weighing_id_uniq",
            "unique(weighing_id)",
            "A weighing line with this Weighing ID already exists.",
        ),
    ]

    def write(self, vals):  # pylint: disable=method-required-super
        # Append-only: a weighing line can never be modified after creation,
        # through any path (UI, RPC, sudo or the developer-mode superuser).
        # This guarantee is the whole point of the model, so there is no
        # context flag to bypass it. Direct SQL is out of scope by design.
        raise AccessError(_("Weighing lines are append-only and cannot be modified."))

    def unlink(self):  # pylint: disable=method-required-super
        # Append-only: deletion is denied for everyone, through any path.
        # The parent product cannot be deleted either while lines exist
        # (product_tmpl_id ondelete="restrict"), so the trail is preserved.
        raise AccessError(_("Weighing lines are append-only and cannot be deleted."))
