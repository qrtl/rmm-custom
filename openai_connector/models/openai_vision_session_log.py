import json
import logging
from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class OpenAISessionLog(models.Model):
    _name = "openai.vision.session.log"
    _description = "OpenAI Vision Session Log"
    _order = "create_date desc"

    session_name = fields.Char(string="Session Name", required=True)
    refusal_message = fields.Text(string="Refusal Message")
    error_message = fields.Text(string="Error Message")
    request_payload = fields.Text(string="Request Payload (sanitized)", required=True)

    @api.model
    def create_from_session(self, session, error, refusal):
        log = self.create({
            "session_name": session.name,
            "refusal_message": refusal,
            "error_message": str(error),
            "request_payload": self._strip_images(session.request_payload) or "{}",
        })
        _logger.error(_("OpenAI call failed (Session Name: %s): %s"), session.name, str(error))
        return log
        
    @api.model
    def _strip_images(self, request_payload):
        try:
            clean_payload = json.loads(request_payload)
        except Exception:
            return "{}"
        input_field = clean_payload.get("input", [])
        if isinstance(input_field, list):
            for message in input_field:
                for part in message.get("content", []):
                    if isinstance(part, dict) and part.get("type") == "image_url":
                        part["image_url"] = {"url": "REMOVED_FOR_LOG"}
        return json.dumps(clean_payload, indent=2)

