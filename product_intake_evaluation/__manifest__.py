# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Intake Evaluation Product",
    "category": "Intake Evaluation Product",
    "version": "15.0.1.0.0",
    "author": "Quartile",
    "website": "https://www.quartile.co",
    "license": "AGPL-3",
    "depends": [
        "purchase_stock",
        "product_state",
        "base_group_backend",
    ],
    "data": [
        "views/product_template_intake_evaluation_views.xml",
        "views/intake_evaluation_board_views.xml",
        "security/delivery_security.xml",
        "security/ir.model.access.csv",
        "data/intake_evaluation_board_data.xml",
        "data/menu_item_data.xml",
        "views/product_template_views.xml",
        "views/res_users_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
}
