# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests import common
from odoo.tools import mute_logger


class TestProductWeighing(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.WeighingLine = cls.env["product.weighing.line"]
        cls.product = cls.env["product.template"].create({"name": "Test Product"})
        group_user = cls.env.ref("base.group_user")
        group_integration = cls.env.ref("product_weighing.group_weighing_integration")
        group_system = cls.env.ref("base.group_system")
        cls.integration_user = cls.env["res.users"].create(
            {
                "name": "Weighing API",
                "login": "weighing_api",
                "groups_id": [Command.set([group_user.id, group_integration.id])],
            }
        )
        cls.regular_user = cls.env["res.users"].create(
            {
                "name": "Regular",
                "login": "weighing_regular",
                "groups_id": [Command.set([group_user.id])],
            }
        )
        cls.admin_user = cls.env["res.users"].create(
            {
                "name": "Admin",
                "login": "weighing_admin",
                "groups_id": [Command.set([group_user.id, group_system.id])],
            }
        )

    def _line_vals(
        self, weighing_id, net_weight=20.70, measured_at="2026-07-13 09:41:18"
    ):
        return {
            "product_tmpl_id": self.product.id,
            "weighing_id": weighing_id,
            "measured_at": measured_at,
            "measurer_name": "Yamada",
            "receipt_no": "R-20260713-118",
            "gross_weight": 45.20,
            "dust_detail": "cage cart x2, cart x1",
            "dust_weight": 24.50,
            "net_weight": net_weight,
            "image_hash": "a3f1c9e0,91d44b0a",
        }

    def test_access_control(self):
        # Create is restricted to the integration group.
        line = self.WeighingLine.with_user(self.integration_user).create(
            self._line_vals("WEIGH-KNG-20260713-0004")
        )
        self.assertTrue(line.exists())
        for user in (self.regular_user, self.admin_user):
            with self.assertRaises(AccessError):
                self.WeighingLine.with_user(user).create(
                    self._line_vals("WEIGH-KNG-20260713-9%s" % user.id)
                )
        # Lines are append-only: write and unlink are blocked for every user,
        # including integration and admin. The model overrides write/unlink to
        # always raise AccessError, so the block also holds for sudo and the
        # developer-mode superuser (no ACL bypass and no context flag to escape
        # it), consistent with the access denial the ACL already returns.
        for user in (self.integration_user, self.regular_user, self.admin_user):
            with self.assertRaises(AccessError):
                line.with_user(user).write({"measurer_name": "Tampered"})
            with self.assertRaises(AccessError):
                line.with_user(user).unlink()
        with self.assertRaises(AccessError):
            line.sudo().write({"measurer_name": "Tampered"})
        with self.assertRaises(AccessError):
            line.sudo().unlink()
        # The parent product cannot be deleted while a line references it
        # (product_tmpl_id ondelete="restrict"), so the trail is preserved
        # instead of being erased by cascade.
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            self.product.with_user(self.admin_user).unlink()
            self.product.flush()

    def test_weighing_id_uniqueness(self):
        self.WeighingLine.create(self._line_vals("WEIGH-KNG-20260713-0007"))
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            self.WeighingLine.create(self._line_vals("WEIGH-KNG-20260713-0007"))
            self.WeighingLine.flush()

    def test_product_aggregates(self):
        lines = self.WeighingLine
        lines |= self.WeighingLine.create(
            self._line_vals("WEIGH-KNG-20260713-0010", net_weight=20.70)
        )
        lines |= self.WeighingLine.create(
            self._line_vals("WEIGH-KNG-20260713-0011", net_weight=18.80)
        )
        lines |= self.WeighingLine.create(
            self._line_vals("WEIGH-KNG-20260714-0021", net_weight=14.80)
        )
        self.assertEqual(self.product.weighing_count, 3)
        self.assertAlmostEqual(self.product.total_net_weight, 54.30, places=2)
        self.assertEqual(
            self.product.weighing_confirmed_at,
            max(lines.mapped("create_date")),
        )
