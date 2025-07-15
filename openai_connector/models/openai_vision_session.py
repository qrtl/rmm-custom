# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class OpenaiVisionSession(models.Model):
    _name = "openai.vision.session"
    _inherit = ["api.call.mixin"]
    _description = "OpenAI Vision Session"

    name = fields.Char(required=True)
    model = fields.Selection(
        [("gpt-4o", "GPT-4o")],
        default="gpt-4o",
        required=True,
    )
    temperature = fields.Float(
        default=0.7,
        help="Sets response randomness (0–2). Higher is more creative, lower is more focused.",
    )
    instruction = fields.Text(
        help="System-level instruction for the assistant."
        "\nExample: You are a helpful assistant that answers in Japanese."
    )
    previous_response_id = fields.Char(
        string="Previous Response ID",
        help="ID of previous response to continue chat (expires in 30 days).",
    )
    store_response = fields.Boolean()
    web_search = fields.Boolean(string="Use Web Search")
    response_format_enabled = fields.Boolean(
        string="Use Structured Output (JSON Schema)"
    )
    response_format_schema = fields.Text(
        string="Response Format Schema (JSON)",
        default=lambda self: json.dumps(
            {
                "type": "object",
                "properties": {"message": {"type": "string"}},
                "required": ["message"],
                "additionalProperties": False,
                "strict": True,
            },
            indent=2,
        ),
    )

    @api.constrains("response_format_schema")
    def _constrains_response_format_schema(self):
        for record in self:
            try:
                json.loads(record.response_format_schema or "{}")
            except json.JSONDecodeError as e:
                raise UserError(_("The JSON schema is invalid:\n{}").format(e)) from e

    def _get_request_payload(self, input_datas):
        self.ensure_one()
        try:
            request_payload = {
                "model": self.model,
                "instructions": self.instruction or "",
                "input": json.loads(input_datas) or [],
                "temperature": self.temperature,
                "store": self.store_response,
                "tools": [{"type": "web_search_preview"}] if self.web_search else [],
            }
            if self.response_format_enabled:
                schema = json.loads(self.response_format_schema or "{}")
                request_payload["text"] = {
                    "format": {
                        "type": "json_schema",
                        "name": "json_schema",
                        "schema": schema,
                    }
                }
            if self.previous_response_id:
                request_payload["previous_response_id"] = self.previous_response_id
            return request_payload
        except Exception as e:
            raise UserError(
                _("Failed to compute request_payload for session %(id)s: %(error)s")
                % {"id": self.id, "error": e}
            ) from e

    def call_openai(self, input_datas):
        self.ensure_one()
        payload = self._get_request_payload(input_datas)
        try:
            response = self.make_api_call(
                "openai",
                endpoint="v1/responses",
                json=payload,
                http_method="post",
            )
            response_json = response.json()
            refusal = response_json.get("refusal_reason")
            if refusal:
                raise UserError(_("OpenAI refused the request:\n{}").format(refusal))
            if self.store_response:
                self.previous_response_id = response_json.get("id")
            output = response_json.get("output", [])
            contents = []
            for item in output:
                contents.extend(item.get("content", []))
            return contents[0].get("text")
        except Exception as e:
            raise UserError(_("OpenAI error:\n{}").format(e)) from e
