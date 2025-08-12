# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tools.sql import column_exists


def pre_init_hook(cr):
    if not column_exists(cr, "product_template", "branch_id"):
        cr.execute(
            """
            ALTER TABLE product_template
            ADD COLUMN branch_id INTEGER REFERENCES product_template(id) ON DELETE SET NULL;
            """
        )
