# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    is_image_attachment_zip = fields.Boolean()

    @api.model
    def _cron_delete_product_image_zip(self):
        zip_attachment = self.search([("is_image_attachment_zip", "=", True)])
        zip_attachment.unlink()
