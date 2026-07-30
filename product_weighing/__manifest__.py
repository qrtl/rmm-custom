# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Weighing",
    "summary": "Append-only weighing lines linked to products for tamper-proof records",
    "category": "Product",
    "version": "15.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "AGPL-3",
    "depends": ["product"],
    "data": [
        "security/product_weighing_security.xml",
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
    ],
    "installable": True,
}
