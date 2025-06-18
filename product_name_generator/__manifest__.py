# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Product Name Generator",
    "version": "15.0.1.0.0",
    "author": "Quatile",
    "license": "AGPL-3",
    "website": "https://www.quartile.co",
    "depends": ["website_sale", "queue_job", "openai_connector"],
    "data": [
        "data/session.xml",
        "views/product_image_views.xml",
    ],
    "installable": True,
}
