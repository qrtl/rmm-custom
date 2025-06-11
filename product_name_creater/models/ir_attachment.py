#example how to use this module
import base64
import json
from odoo.exceptions import UserError

from odoo import api, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def analyze_with_openai_vision(
        self,
        attachment_id,
    ):
        attachment = self.browse(attachment_id)
        if not attachment or not attachment.datas:
            return "There is no attachment"

        image_data = base64.b64decode(attachment.datas)
        base64_str = base64.b64encode(image_data).decode("utf-8")
        input_image = f"data:{attachment.mimetype};base64,{base64_str}"
        session = self.env.ref("product_name_creater.openai_vision_session_product_name_creater")
        session.inputs = json.dumps([
            {
                "role": "user",
                "content": [
                    {"type": "input_image", "image_url": input_image}
                ]
            }
        ], indent=2)

        response_json_str = session.call_openAI()
        response_json = json.loads(response_json_str)
        product_name = response_json.get("product_name")

        return product_name
