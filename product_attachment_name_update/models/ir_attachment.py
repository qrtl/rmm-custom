# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model_create_multi
    def create(self, vals_list):
        attachments = super(IrAttachment, self).create(vals_list)
        for attachment in attachments:
            if (
                attachment.res_model
                in [
                    "product.template",
                    "product.product",
                ]
                and not attachment.res_field
            ):
                if attachment.res_model == "product.template":
                    res_model = "product.template"
                else:
                    res_model = "product.product"
                rec = self.env[res_model].browse(attachment.res_id)
                attachment.name = f"[{rec.name}][{attachment.id}] {attachment.name}"
        return attachments
