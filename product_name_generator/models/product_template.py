# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json

from odoo import _, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    openai_generated_name = fields.Char()

    def call_openAI(self, session):
        response_json_str = session.call_openAI()
        response_json = json.loads(response_json_str)
        product_name = response_json.get("product_name")
        self.with_context(lang="ja_JP").product_tmpl_id.name = product_name

    def action_generate_product_name(self):
        if not self.image_1920:
            raise UserError(_("Please upload the image first."))
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        input_image = f"{base_url}/web/image/{self._name}/{self.id}/image_1920"
        session = self.env.ref(
            "product_name_generator.openai_vision_session_product_name_generator"
        )
        session.inputs = json.dumps(
            [
                {
                    "role": "user",
                    "content": [{"type": "input_image", "image_url": input_image}],
                }
            ]
        )
        self.with_delay().call_openAI(session)
