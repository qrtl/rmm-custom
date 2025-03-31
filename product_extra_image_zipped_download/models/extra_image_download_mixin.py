# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models


class ExtraImageDownloadMixin(models.Model):
    _name = "extra.image.download.mixin"

    def _download_product_images_zip(self):
        model_name = self._name
        ids_str = ",".join(map(str, self.ids))
        return {
            "type": "ir.actions.act_url",
            "url": f"/download/product/images?ids={ids_str}&model={model_name}",
            "target": "self",
        }
