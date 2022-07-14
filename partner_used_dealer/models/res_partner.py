# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    identification_type_id = fields.Many2one(
        comodel_name="res.identification.type", string="Identification Type",
    )
    identification_number = fields.Char(string="Identification Number",)
    occupation_id = fields.Many2one("res.occupation", "Occupation")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    date_of_birth = fields.Date("Date of Birth")
    fax = fields.Char()
    