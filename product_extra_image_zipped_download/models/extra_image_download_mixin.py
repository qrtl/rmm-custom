# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import io
import zipfile
from datetime import datetime

from odoo import models


class ExtraImageDownloadMixin(models.Model):
    _name = "extra.image.download.mixin"

    def _download_product_images_zip(self):
        # This is only intended for product.product and product.template because
        # they display the same field, product_template_image_ids, in the UI.
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            extra_images = self.product_template_image_ids
            for img in extra_images:
                image_data = base64.b64decode(img.image_1920)
                filename = f"[{img.id}] {img.img_name}"
                zipf.writestr(filename, image_data)
        zip_buffer.seek(0)
        zip_base64 = base64.b64encode(zip_buffer.read())
        today_str = datetime.today().strftime("%Y_%m_%d")
        zip_filename = f"[{today_str}]_product_extra_images.zip"
        attachment = self.env["ir.attachment"].create(
            {
                "name": zip_filename,
                "type": "binary",
                "datas": zip_base64,
                "mimetype": "application/zip",
                "res_model": "product.template",
                "is_image_attachment_zip": True,
                "res_id": self[0].id,
            }
        )
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "self",
        }
