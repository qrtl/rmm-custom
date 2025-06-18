# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Openai Connector",
    "version": "15.0.1.0.0",
    "author": "Quatile",
    "license": "AGPL-3",
    "website": "https://www.quartile.co",
    "depends": ["web"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/openai_vision_session_view.xml",
    ],
    "external_dependencies": {
        "python": ["openai"],
    },
    "installable": True,
}
