# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _compute_message_attachment_count(self):
        super()._compute_message_attachment_count()
        related_model_map = {
            "product.template": ("product.product", "product_variant_id"),
            "product.product": ("product.template", "product_tmpl_id"),
        }
        related_model, related_field = related_model_map.get(self._name, (None, None))
        if not related_model or not related_field:
            return
        related_records = self.mapped(related_field)
        if not related_records:
            return
        read_group_var = self.env["ir.attachment"].read_group(
            [("res_id", "in", related_records.ids), ("res_model", "=", related_model)],
            fields=["res_id"],
            groupby=["res_id"],
        )
        attachment_count_dict = {d["res_id"]: d["res_id_count"] for d in read_group_var}
        for record in self:
            related_id = record[related_field].id
            record.message_attachment_count += attachment_count_dict.get(related_id, 0)
