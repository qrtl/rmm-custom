# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Intake Evaluation Product",
    "category": "Auction",
    "version": "15.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "LGPL-3",
    "depends": [
        "product_state",
        "base_group_backend",
        "purchase_stock",
    ],
    "data": [
        "views/product_template_intake_evaluation_views.xml",
        "views/intake_evaluation_board_views.xml",
        "security/delivery_security.xml",
        "security/ir.model.access.csv",
        "data/intake_evaluation_board_data.xml",
        "data/menu_item_data.xml",
        "views/valuation_status_views.xml",
        "views/product_template_views.xml",
        "views/res_users_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
