# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    is_intake_evaluation_user = fields.Boolean(
        compute="_compute_is_intake_evaluation_user",
        inverse="_inverse_is_intake_evaluation_user",
    )
    is_intake_evaluation_manager = fields.Boolean(
        compute="_compute_is_intake_evaluation_manager",
        inverse="_inverse_is_intake_evaluation_manager",
    )

    # --- Intake Evaluation User ---
    def _compute_is_intake_evaluation_user(self):
        for user in self:
            user.is_intake_evaluation_user = user.has_group(
                "product_intake_evaluation.group_intake_evaluation_user"
            )

    def _inverse_is_intake_evaluation_user(self):
        group = self.env.ref("product_intake_evaluation.group_intake_evaluation_user")
        for user in self:
            if user.is_intake_evaluation_user:
                user.groups_id = [Command.link(group.id)]
                user.partner_id.is_intake_evaluation_partner = True
            else:
                user.groups_id = [Command.unlink(group.id)]

    # --- Intake Evaluation Manager ---
    def _compute_is_intake_evaluation_manager(self):
        for user in self:
            user.is_intake_evaluation_manager = user.has_group(
                "product_intake_evaluation.group_intake_evaluation_manager"
            )

    def _inverse_is_intake_evaluation_manager(self):
        group = self.env.ref(
            "product_intake_evaluation.group_intake_evaluation_manager"
        )
        for user in self:
            if user.is_intake_evaluation_manager:
                user.groups_id = [Command.link(group.id)]
                user.partner_id.is_intake_evaluation_partner = True
            else:
                user.groups_id = [Command.unlink(group.id)]
