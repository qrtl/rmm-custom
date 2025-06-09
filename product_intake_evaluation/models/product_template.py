# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.exceptions import AccessError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_default_status_id(self):
        return self.env['valuation.status'].search([], limit=1) or False

    valuation_status_id = fields.Many2one('valuation.status',ondelete='restrict',default=_get_default_status_id,copy=False)
    assigned_branch_id = fields.Many2one("res.partner")
    carrier_contact_person = fields.Char()
    tracking_no_1 = fields.Char()
    tracking_no_2 = fields.Char()
    valuation_comment = fields.Text()

    @api.model
    def create(self, vals):
        ctx = self.env.context
        if ctx.get('update_branch') and not vals.get('assigned_branch_id'):
            partner_id = self.env.user.partner_id.id
            if partner_id:
                vals['assigned_branch_id'] = partner_id
        return super().create(vals)

    def write(self, vals):
        if 'valuation_status_id' in vals:
            if not self.env.user.has_group('product_intake_evaluation.group_intake_evaluation_admin'):
                raise AccessError("You do not have permission to modify the valuation status.")
        return super().write(vals)
