# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json

from odoo import _, models
from odoo.exceptions import UserError

IMAGE_TYPES = ["image/png", "image/jpeg", "image/bmp", "image/tiff"]


class ProductImage(models.Model):
    _inherit = "product.image"

    def call_openAI(self, session):
        response_json_str = session.call_openAI()
        response_json = json.loads(response_json_str)
        product_name = response_json.get("product_name")
        self.with_context(lang="ja_JP").product_tmpl_id.name = product_name

    def action_generate_product_name(self):
        if not self.image_1920:
            raise UserError(_("Please upload the image first."))
        attachment = self.env["ir.attachment"].search(
            [
                ("res_id", "=", self.id),
                ("res_model", "=", "product.image"),
                ("res_field", "=", "image_1920"),
                ("mimetype", "in", IMAGE_TYPES),
            ],
            limit=1,
        )
        if not attachment:
            raise UserError(_("There is no attachment for this product image."))
        input_image = f"data:{attachment.mimetype};base64,{attachment.datas}"
        session = self.env.ref(
            "product_name_generator.openai_vision_session_product_name_generator"
        )
        session.inputs = [
            {
                "role": "user",
                "content": [{"type": "input_image", "image_url": input_image}],
            }
        ]
        self.with_delay().call_openAI(session)
