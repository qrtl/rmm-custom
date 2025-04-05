# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import mimetypes

from odoo import api, fields, models
from odoo.tools.mimetypes import get_extension, guess_mimetype


class ProductImage(models.Model):
    _inherit = "product.image"

    img_name = fields.Char("Image Name")

    def _get_image_name(self):
        self.ensure_one()
        if self.img_name:
            return self.img_name
        image_name = self.name
        extension = get_extension(image_name)
        if not extension:
            image_data = base64.b64decode(self.image_1920)
            mimetype = guess_mimetype(image_data)
            extension = mimetypes.guess_extension(mimetype)
            image_name = f"{image_name}{extension}"
        # TODO: Assignment of self.id in the image name should be done in another module
        return f"{self.id}{image_name}"

    def _assign_image_name(self):
        self.ensure_one()
        self.img_name = self._get_image_name()

    @api.model
    def create(self, vals):
        res = super().create(vals)
        for rec in res:
            rec._assign_image_name()
        return res

    def write(self, vals):
        res = super().write(vals)
        if "name" in vals:
            # Reset the image name to force re-calculation
            for rec in self:
                rec.img_name = False
                rec._assign_image_name()
        return res
