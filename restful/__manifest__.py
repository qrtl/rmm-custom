{
    "name": "Odoo RESTFUL API",
    "version": "15.0.1.2.0",
    "category": "API",
    "author": "Babatope Ajepe, Quartile Limited",
    "website": "https://www.quartile.co",
    "summary": "Odoo RESTFUL API",
    "support": "ajepebabatope@gmail.com",
    "depends": ["web", "base_setup"],
    "data": [
        "views/ir_model.xml",
        "views/res_users.xml",
        "security/ir.model.access.csv",
    ],
    "images": ["static/description/main_screenshot.png"],
    "license": "LGPL-3",
    "installable": True,
    "auto_install": False,
}
