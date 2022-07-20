# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResOccupation(models.Model):
    _name = "res.occupation"

    name = fields.Char(required=True)
