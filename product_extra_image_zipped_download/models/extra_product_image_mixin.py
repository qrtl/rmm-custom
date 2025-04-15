# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models


class ExtraProductImageMixin(models.Model):
    _name = "extra.product.image.mixin"

    def _download_product_images_zip(self):
        model_name = self._name
        ids_str = ",".join(map(str, self.ids))
        return {
            "type": "ir.actions.act_url",
            "url": f"/download/product/images?ids={ids_str}&model={model_name}",
            "target": "self",
        }

    # TODO: To be split into a separate module
    def export_data(self, fields_to_export):
        images = self.env["product.image"].browse()
        if "product_variant_image_ids/img_name" in fields_to_export:
            images += self.product_variant_image_ids
        if "product_template_image_ids/img_name" in fields_to_export:
            images += self.product_template_image_ids
        images = images.filtered(lambda x: not x.img_name)
        for img in images:
            img._assign_image_name()
        return super().export_data(fields_to_export)
