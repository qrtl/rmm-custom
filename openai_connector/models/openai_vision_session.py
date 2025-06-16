import json
import logging

from openai import OpenAI

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class OpenAISession(models.Model):
    _name = "openai.vision.session"
    _description = "OpenAI Vision Session"

    name = fields.Char(required=True)
    model = fields.Selection(
        [
            ("gpt-4o", "GPT-4o"),
        ],
        default="gpt-4o",
        required=True,
    )
    temperature = fields.Float(default=0.7)
    instruction = fields.Text()
    inputs = fields.Text()
    previous_response_id = fields.Char(string="Previous Response ID")
    store_response = fields.Boolean(default=True)
    web_search = fields.Boolean(string="Use Web Search", default=False)
    response_format_enabled = fields.Boolean(
        string="Use Structured Output (JSON Schema)", default=False
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
    request_payload = fields.Text(compute="_compute_request_payload", store=False)

    @api.onchange("response_format_schema")
    def _onchange_response_format_schema(self):
        for record in self:
            if record.response_format_enabled:
                try:
                    json.loads(record.response_format_schema or "{}")
                except json.JSONDecodeError as e:
                    raise UserError(
                        _("The JSON schema is invalid:\n{}").format(e)
                    ) from e

    def _compute_request_payload(self):
        self.ensure_one()
        try:
            request_payload = {
                "model": self.model,
                "instructions": self.instruction or "",
                "input": json.loads(self.inputs or "[]"),
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
            self.request_payload = json.dumps(request_payload, indent=2)
        except Exception as e:
            raise UserError(
                _("Failed to compute request_payload for session %(id)s: %(error)s")
                % {
                    "id": self.id,
                    "error": e,
                }
            ) from e

    @api.model
    def call_openAI(self):
        self.ensure_one()
        api_key = self.env.company.openai_api_key
        if not api_key:
            raise UserError(_("OpenAI API key is not configured"))
        client = OpenAI(api_key=api_key)
        refusal = False
        try:
            payload = json.loads(self.request_payload)
            response = client.responses.create(**payload)
            if self.store_response:
                self.previous_response_id = getattr(response, "id", False)
            refusal = getattr(response, "refusal_reason", None)
            if refusal:
                raise UserError(_("OpenAI refused the request:\n{}").format(refusal))
            output = getattr(response, "output_text", "") or ""
            return output.strip()

        except Exception as e:
            raise UserError(_("OpenAI error:\n{}").format(e)) from e
