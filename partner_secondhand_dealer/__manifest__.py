# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Partner Secondhand Dealer",
    "category": "Purchase",
    "version": "15.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "LGPL-3",
    "depends": ["purchase"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_identification_type_views.xml",
        "views/res_occupation_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
