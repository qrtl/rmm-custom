from odoo import models, fields

class Users(models.Model):
    _inherit = "res.users"

    is_delivery_carrier_user = fields.Boolean(
        compute="_compute_is_delivery_carrier_user",
        inverse="_inverse_is_delivery_carrier_user"
    )
    is_delivery_carrier_manager = fields.Boolean(
        compute="_compute_is_delivery_carrier_manager",
        inverse="_inverse_is_delivery_carrier_manager"
    )

    # --- Delivery Carrier User ---
    def _compute_is_delivery_carrier_user(self):
        for user in self:
            user.is_delivery_carrier_user = user.has_group("delivery_carrier_product.group_delivery_carrier_user")

    def _inverse_is_delivery_carrier_user(self):
        group = self.env.ref("delivery_carrier_product.group_delivery_carrier_user")
        for user in self:
            if user.is_delivery_carrier_user:
                user.groups_id = [(4, group.id)]
            else:
                user.groups_id = [(3, group.id)]

    # --- Delivery Carrier Manager ---
    def _compute_is_delivery_carrier_manager(self):
        for user in self:
            user.is_delivery_carrier_manager = user.has_group("delivery_carrier_product.group_delivery_carrier_manager")

    def _inverse_is_delivery_carrier_manager(self):
        group = self.env.ref("delivery_carrier_product.group_delivery_carrier_manager")
        for user in self:
            if user.is_delivery_carrier_manager:
                user.groups_id = [(4, group.id)]
            else:
                user.groups_id = [(3, group.id)]
