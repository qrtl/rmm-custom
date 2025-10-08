# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OpenAIVisionSession(models.Model):
    _inherit = "openai.vision.session"

    reference_code = fields.Selection(
        selection_add=[("product_name_generation", "Product Name Generation")],
        ondelete={"product_name_generation": "cascade"},
    )
