# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sales Order Import",
    "version": "15.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Sales Management",
    "license": "AGPL-3",
    "depends": [
        "sale_stock",
        "base_data_import",
        "sale",
        "delivery",
        "queue_job",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/data_import_logs_views.xml",
        "views/sale_import_default.xml",
        "views/sale_order_views.xml",
        "wizard/import_sale_view.xml",
    ],
    "installable": True,
}