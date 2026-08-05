# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo import Command, fields
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

    def _force_create_date(self, line, value):
        # create_date is assigned by the ORM from cr.now(), which is cached for
        # the whole transaction and never reset by a savepoint rollback, so
        # every record a test creates shares one timestamp. Forcing the column
        # is the only way to give lines distinct creation times and actually
        # exercise the max() in the weighing_confirmed_at compute.
        self.env.cr.execute(
            "UPDATE product_weighing_line SET create_date = %s WHERE id = %s",
            (value, line.id),
        )
        line.invalidate_cache(["create_date"], line.ids)
        line.modified(["create_date"])

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
        with self.assertRaises(IntegrityError), mute_logger(
            "odoo.sql_db"
        ), self.cr.savepoint():
            self.product.with_user(self.admin_user).unlink()
        self.assertTrue(self.product.exists())

    def test_weighing_id_uniqueness(self):
        self.WeighingLine.create(self._line_vals("WEIGH-KNG-20260713-0007"))
        with self.assertRaises(IntegrityError), mute_logger(
            "odoo.sql_db"
        ), self.cr.savepoint():
            self.WeighingLine.create(self._line_vals("WEIGH-KNG-20260713-0007"))
        # The constraint is global, not per product: the same external weighing
        # ID cannot be recorded against a second product either.
        other_product = self.env["product.template"].create({"name": "Other Product"})
        with self.assertRaises(IntegrityError), mute_logger(
            "odoo.sql_db"
        ), self.cr.savepoint():
            self.WeighingLine.create(
                dict(
                    self._line_vals("WEIGH-KNG-20260713-0007"),
                    product_tmpl_id=other_product.id,
                )
            )
        self.assertEqual(
            self.WeighingLine.search_count(
                [("weighing_id", "=", "WEIGH-KNG-20260713-0007")]
            ),
            1,
        )

    def test_product_aggregates(self):
        self.assertEqual(self.product.weighing_count, 0)
        self.assertFalse(self.product.total_net_weight)
        self.assertFalse(self.product.weighing_confirmed_at)
        line_1 = self.WeighingLine.create(
            self._line_vals(
                "WEIGH-KNG-20260713-0010",
                net_weight=20.70,
                measured_at="2026-07-13 09:41:18",
            )
        )
        line_2 = self.WeighingLine.create(
            self._line_vals(
                "WEIGH-KNG-20260713-0011",
                net_weight=18.80,
                measured_at="2026-07-13 14:05:02",
            )
        )
        line_3 = self.WeighingLine.create(
            self._line_vals(
                "WEIGH-KNG-20260714-0021",
                net_weight=14.80,
                measured_at="2026-07-14 08:12:44",
            )
        )
        # Deliberately out of both creation order and measured_at order: line_2
        # is recorded last, while line_3 was created last and has the latest
        # measured_at. A compute using min(), the first or last line of the
        # one2many, or max(measured_at) would each yield a different value than
        # the one asserted below.
        self._force_create_date(line_1, "2026-07-20 01:00:00")
        self._force_create_date(line_2, "2026-07-22 02:00:00")
        self._force_create_date(line_3, "2026-07-21 03:00:00")
        self.assertEqual(self.product.weighing_count, 3)
        self.assertAlmostEqual(self.product.total_net_weight, 54.30, places=2)
        self.assertEqual(
            self.product.weighing_confirmed_at,
            fields.Datetime.to_datetime("2026-07-22 02:00:00"),
        )
        self.assertEqual(self.product.weighing_confirmed_at, line_2.create_date)

    def test_company_isolation(self):
        company_b = self.env["res.company"].create({"name": "Weighing Company B"})
        product_b = self.env["product.template"].create(
            {"name": "Company B Product", "company_id": company_b.id}
        )
        line_b = self.WeighingLine.create(
            dict(
                self._line_vals("WEIGH-KNG-20260713-0030"),
                product_tmpl_id=product_b.id,
            )
        )
        self.assertEqual(line_b.company_id, company_b)
        # The integration user belongs to the default company only, so the
        # multi-company rule hides Company B's line on read...
        self.assertNotIn(
            line_b, self.WeighingLine.with_user(self.integration_user).search([])
        )
        # ...and blocks creating a line against a product of a company it has
        # no access to, which would otherwise mutate that product's stored
        # aggregates through the recompute.
        with self.assertRaises(AccessError):
            self.WeighingLine.with_user(self.integration_user).create(
                dict(
                    self._line_vals("WEIGH-KNG-20260713-0031"),
                    product_tmpl_id=product_b.id,
                )
            )
        # A line on a company-shared product stays readable by every internal
        # user, which is what the base.group_user read grant is there for.
        shared_line = self.WeighingLine.create(
            self._line_vals("WEIGH-KNG-20260713-0032")
        )
        self.assertFalse(shared_line.company_id)
        for user in (self.integration_user, self.regular_user):
            self.assertIn(shared_line, self.WeighingLine.with_user(user).search([]))
