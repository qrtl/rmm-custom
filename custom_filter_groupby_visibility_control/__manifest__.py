# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Custom Filter GroupBy Visibility Control",
    "category": "Tools",
    "version": "15.0.1.0.0",
    "author": "Quartile",
    "website": "https://www.quartile.co",
    "license": "AGPL-3",
    "depends": ["web"],
    "data": [
        "security/custom_filter_groupby_security.xml",
    ],
    "assets": {
        "web.assets_qweb": [
            "custom_filter_groupby_visibility_control/static/src/xml/*.xml",
        ],
        "web.assets_backend": [
            "custom_filter_groupby_visibility_control/static/src/js/*.esm.js",
        ],
    },
    "installable": True,
}
