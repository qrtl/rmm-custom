# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "OpenAI Connector",
    "version": "15.0.1.0.0",
    "author": "Quartile",
    "license": "AGPL-3",
    "website": "https://www.quartile.co",
    "depends": ["base_api_connection"],
    "data": [
        "data/api_config.xml",
        "security/ir.model.access.csv",
        "views/openai_vision_session_views.xml",
    ],
    "installable": True,
}
