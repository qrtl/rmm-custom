# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Name Generator",
    "version": "15.0.1.0.0",
    "author": "Quatile",
    "license": "AGPL-3",
    "website": "https://www.quartile.co",
    "depends": ["website_sale", "openai_connector", "queue_job"],
    "data": [
        "data/ir_config_parameter.xml",
        "data/openai_vision_session.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
}
