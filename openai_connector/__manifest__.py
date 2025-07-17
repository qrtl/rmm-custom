# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Openai Connector",
    "version": "15.0.1.0.0",
    "author": "Quartile",
    "license": "LGPL-3",
    "website": "https://www.quartile.co",
    "depends": ["base_api_connection"],
    "data": [
        "data/base_api_connection.xml",
        "security/ir.model.access.csv",
        "views/openai_vision_session_views.xml",
    ],
    "installable": True,
}
