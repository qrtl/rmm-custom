from odoo import api, fields, models


class OpenAIVisionMessage(models.Model):
    _name = "openai.vision.message"
    _description = "OpenAI Vision Message Line"

    role = fields.Selection(
        [("user", "User"), ("assistant", "Assistant")], default="user", required=True
    )
    type = fields.Selection(
        [("input_text", "Text"), ("input_image", "Image URL")],
        default="input_text",
        required=True,
    )
    input_session_id = fields.Many2one("openai.vision.session", string="Input Session")
    response_session_id = fields.Many2one(
        "openai.vision.session", string="Response Session"
    )
    content = fields.Text(
        required=True,
    )
    sequence = fields.Integer(default=10)

    @api.model
    def to_openai_dict(self):
        if self.type == "input_text":
            return {
                "type": "input_text",
                "text": self.content.strip() if self.content else "",
            }
        elif self.type == "input_image":
            url = self.content.strip() if self.content else ""
            return {"type": "input_image", "image_url": url}
