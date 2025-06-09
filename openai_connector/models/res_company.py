from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    openai_api_key = fields.Char(string="OpenAI API Key")
