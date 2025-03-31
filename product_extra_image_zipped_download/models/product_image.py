# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import mimetypes

from odoo import api, fields, models
from odoo.tools.mimetypes import get_extension, guess_mimetype


class ProductImage(models.Model):
    _inherit = "product.image"

    img_name = fields.Char("Image Name")
    update_imge_name = fields.Boolean()

    @api.model
    def create(self, vals):
        res = super().create(vals)
        for rec in res:
            image_name = rec.img_name
            if not rec.img_name:
                name = rec.name
                image_data = base64.b64decode(rec.image_1920)
                mimetype = guess_mimetype(image_data)
                extension = get_extension(name)
                if not extension:
                    extension = mimetypes.guess_extension(mimetype)
                image_name = f"{name}{extension}" if extension else name
            rec.img_name = f"[{rec.id}] {image_name}"
        return res

    @api.model
    def _cron_update_product_image(self, limit):
        images = self.search(
            [("img_name", "=", False), ("update_imge_name", "=", False)], limit=limit
        )
        for img in images:
            name = img.name
            image_data = base64.b64decode(img.image_1920)
            mimetype = guess_mimetype(image_data)
            extension = get_extension(img.name)
            if extension:
                img.img_name = name
                continue
            extension = mimetypes.guess_extension(mimetype)
            img.img_name = f"[{img.id}] {name}{extension}"
            img.update_imge_name = True
