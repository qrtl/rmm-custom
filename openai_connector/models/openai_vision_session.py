import json
from odoo import models, fields, api
from odoo.exceptions import UserError
from openai import OpenAI
from collections import defaultdict

class OpenAISession(models.Model):
    _name = 'openai.vision.session'
    _description = 'OpenAI Vision Session'

    name = fields.Char(required=True, string="Session Name")
    model = fields.Selection([
        ('gpt-4o', 'GPT-4o'),
    ], default='gpt-4o', required=True)
    temperature = fields.Float(default=0.7, string="Temperature")
    input_message_ids = fields.One2many(
        'openai.vision.message', 'input_session_id', string="Input Messages")
    response_message_ids = fields.One2many(
        'openai.vision.message', 'response_session_id', string="Response Messages")
    previous_response_id = fields.Char(string="Previous Response ID")
    store_response = fields.Boolean(string="Store Response", default=True)
    web_search = fields.Boolean(string="Use Web Search", default=False)
    response_refusal_message = fields.Text(
        string="Refusal Reason", readonly=True)
    response_format_enabled = fields.Boolean(
        string="Use Structured Output (JSON Schema)", default=False)
    response_format_schema = fields.Text(
        string="Response Format Schema (JSON)",
        default=json.dumps({
            "type": "object",
            "properties": {
            "message": {"type": "string"}
            },
            "required": ["message"],
            "additionalProperties": False,
            "strict": True,
            }, 
        indent=2))

    @api.onchange('response_format_schema')
    def _onchange_response_format_schema(self):
        for record in self:
            if record.response_format_enabled:
                try:
                    json.loads(record.response_format_schema or "{}")
                except json.JSONDecodeError as e:
                    raise UserError("The JSON schema is invalid:\n%s" % str(e))

    @api.model
    def call_openAI(self):
        api_key = self.env.company.openai_api_key
        if not api_key:
            raise UserError("OpenAI API key is not configured")

        client = OpenAI(api_key=api_key)

        for record in self:
            if record.model != 'gpt-4o':
                raise UserError(
                    "Responses API（構造化出力）は現在 'gpt-4o' モデルでのみサポートされています。")
            grouped = defaultdict(list)
            for msg in record.input_message_ids:
                key = (msg.sequence, msg.role)
                grouped[key].append(msg)
            instructions = []
            inputs = []
            sorted_keys = sorted(grouped.keys(), key=lambda k: k[0]) 
            for seq, role in sorted_keys:
                components = grouped[(seq, role)]
                roles = {c.role for c in components}
                if len(roles) != 1:
                    raise UserError(f"Multiple roles found at sequence {seq}: {roles}")
                contents = [c.to_openai_dict() for c in components if c.content and c.content.strip()]
                if not contents:
                    continue
                inputs.append({
                    "role": role,
                    "content": contents
                })

            text_format = None
            if record.response_format_enabled:
                try:
                    schema = json.loads(record.response_format_schema or '{}')
                    text_format = {
                        "type": "json_schema",
                        "name": "json_schema",
                        "schema": schema
                    }
                except json.JSONDecodeError as e:
                    raise UserError("Invalid JSON schema:\n%s" % str(e))

            try:
                params = {
                    'model': record.model,
                    'instructions': "\n".join(instructions).strip(),
                    'input': inputs,
                    'temperature': record.temperature,
                    'store': record.store_response,
                    'text': {"format": text_format},
                    "tools": [{"type": "web_search_preview"}] if record.web_search else [],
                }

                if record.previous_response_id:
                    params['previous_response_id'] = record.previous_response_id

                response = client.responses.create(**params)
                if record.store_response:
                    record.previous_response_id = getattr(response, 'id', False)

                refusal = getattr(response, 'refusal_reason', None)
                if refusal:
                    record.response_refusal_message = refusal
                    continue

                record.response_refusal_message = False
                output = getattr(response, 'output_text', '') or ''
                result = output.strip()

                next_seq = max(record.input_message_ids.mapped('sequence') or [0]) + 10
                return_message = record.response_message_ids.create({
                    'response_session_id': record.id,
                    'role': 'assistant',
                    'type': 'input_text',
                    'content': result,
                    'sequence': next_seq,
                })
                return return_message

            except Exception as e:
                raise UserError(f"OpenAI error: {e}")
