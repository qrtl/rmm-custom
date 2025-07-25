# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json

from odoo import _, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    openai_generated_name = fields.Char()

    def generate_name(self, session, base_url):
        is_published = self.is_published
        if not is_published:
            # Need to be published to be accessible to the public.
            self.is_published = True
        input_image = f"{base_url}/web/image/{self._name}/{self.id}/image_1920"
        input_datas = json.dumps(
            [
                {
                    "role": "user",
                    "content": [{"type": "input_image", "image_url": input_image}],
                }
            ]
        )
        response_json_str = session.call_openai(input_datas)
        response_json = json.loads(response_json_str)
        product_name = response_json.get("product_name")
        self.openai_generated_name = product_name
        self.is_published = is_published

    def action_generate_product_name(self):
        session = self.env["openai.vision.session"].search(
            [("reference_code", "=", "product_name_generator")],
            limit=1,
        )
        if not session:
            raise UserError(_("OpenAI Vision Session not found."))
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for rec in self:
            if not rec.image_1920:
                raise UserError(_("Please upload the image first."))
            rec.with_delay().generate_name(session, base_url)
