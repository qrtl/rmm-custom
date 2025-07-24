# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import AccessError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_default_status_id(self):
        if self.env.user.has_group(
            "product_intake_evaluation.group_intake_evaluation_user"
        ):
            return self.env["valuation.status"].search([], limit=1) or False
        return False

    valuation_status = fields.Selection(
        [
            ("before_valuation", "Before Valuation"),
            ("acceptable", "Acceptable"),
            ("need_info", "Need More Information"),
            ("received", "Received"),
            ("unacceptable", "Unacceptable"),
        ]
    )
    branch_id = fields.Many2one("res.partner", compute="_compute_branch_id", store=True)
    sales_office_id = fields.Many2one("res.partner")
    carrier_contact_person = fields.Char()
    tracking_no_1 = fields.Char()
    tracking_no_2 = fields.Char()
    carrier_note = fields.Text()
    valuation_comment = fields.Text()

    @api.depends("sales_office_id")
    def _compute_branch_id(self):
        for product in self:
            if product.sales_office_id:
                product.branch_id = product.sales_office_id.branch_id
            else:
                product.branch_id = False

    # Set default value for intake evaluation user
    @api.model
    def create(self, vals):
        group = self.env.ref("product_intake_evaluation.group_intake_evaluation_user")
        if group not in self.env.user.groups_id:
            return super().create(vals)
        commercial_partner = self.env.user.commercial_partner_id
        if commercial_partner and commercial_partner.is_intake_evaluation_partner:
            vals["sales_office_id"] = commercial_partner.id
        vals["valuation_status"] = "before_valuation"
        return super().create(vals)

    def write(self, vals):
        if "valuation_status" in vals:
            if not self.env.user.has_group(
                "product_intake_evaluation.group_intake_evaluation_admin"
            ):
                raise AccessError(
                    _("You do not have permission to modify the valuation status.")
                )
        return super().write(vals)
