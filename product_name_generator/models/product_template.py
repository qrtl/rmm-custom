# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json

from odoo import _, fields, models
from odoo.exceptions import UserError

from odoo.addons.queue_job.exception import RetryableJobError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    openai_generated_name = fields.Char()

    def generate_name(self, session, base_url, is_published):
        self.ensure_one()
        input_image = f"{base_url}/web/image/{self._name}/{self.id}/image_1920"
        input_datas = json.dumps(
            [
                {
                    "role": "user",
                    "content": [{"type": "input_image", "image_url": input_image}],
                }
            ]
        )
        try:
            response_json_str = session.call_openai(input_datas)
        except UserError as e:
            # HTTP 400 Error about "Timeout while downloading" occurs when calling the
            # OpenAI API to fetch an image. This usually happens if the image takes too
            # long to load or the download is interrupted. In such cases, we treat it as
            # a temporary issue and retry instead of failing permanently.
            # "openai_side_error" is used here because the error message text can be
            # changed from the GUI when the wording changes
            cause = e.__cause__
            openai_side_error = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("product_name_generator.openai.retry.message_substring")
            )
            error_detail = getattr(getattr(cause, "response", None), "text", "")[:500]
            if openai_side_error in error_detail:
                raise RetryableJobError(
                    _("Retry due to OpenAI temporary error"), seconds=60
                ) from None
            raise
        response_json = json.loads(response_json_str)
        product_name = response_json.get("product_name")
        self.openai_generated_name = product_name
        self.is_published = is_published

    def action_generate_product_name(self):
        session = self.env["openai.vision.session"].search(
            [("reference_code", "=", "product_name_generation")],
            limit=1,
        )
        if not session:
            raise UserError(_("OpenAI Vision Session not found."))
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for rec in self:
            if not rec.image_1920:
                raise UserError(_("Please upload the image first."))
            is_published = rec.is_published
            if not is_published:
                # Need to be published to be accessible to the public.
                rec.is_published = True
            rec.with_delay().generate_name(session, base_url, is_published)
