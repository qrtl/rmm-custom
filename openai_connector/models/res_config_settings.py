# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    openai_api_key = fields.Char(
        string="OpenAI API Key",
        related="company_id.openai_api_key",
        readonly=False,
    )
