# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IntakeEvaluationBoard(models.Model):
    _name = "intake.evaluation.board"
    _description = "Intake Evaluation Board"

    name = fields.Char()
    board_type = fields.Selection([("product", "Products")])
