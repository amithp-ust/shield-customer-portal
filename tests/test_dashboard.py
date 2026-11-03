import sqlite3
import unittest
from unittest.mock import Mock

from src.portal.dashboard import CustomerPortal


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)
        self.get_claim = Mock(return_value={
            "claim_id": "CL-1", "policy_id": "P-1",
            "status": "partially_paid", "paid_cents": 40000,
        })
        self.portal = CustomerPortal(
            self.connection,
            lambda policy_id: {"policy_id": policy_id},
            self.get_claim,
            lambda policy_id: {"annual_premium_cents": 5000},
        )

    def test_dashboard(self):
        dashboard = self.portal.dashboard("CL-1")
        self.assertEqual(dashboard["claim"]["status"], "partially_paid")
        self.assertEqual(dashboard["policy"]["policy_id"], "P-1")
        self.assertEqual(dashboard["premium_schedule"]["annual_premium_cents"], 5000)

    def test_local_copy_requires_refresh(self):
        self.portal.refresh_claim("CL-1")
        self.get_claim.return_value["status"] = "paid"
        self.get_claim.return_value["paid_cents"] = 50000
        self.assertEqual(self.portal.cached_claim("CL-1")["status"], "partially_paid")
        self.assertEqual(self.portal.refresh_claim("CL-1")["status"], "paid")
        count = self.connection.execute("SELECT COUNT(*) FROM claim_status").fetchone()[0]
        self.assertEqual(count, 1)

    def test_missing_local_claim(self):
        with self.assertRaises(LookupError):
            self.portal.cached_claim("unknown")

    def test_dependency_failure_is_not_masked_by_cache(self):
        self.portal.refresh_claim("CL-1")
        self.get_claim.side_effect = LookupError("Claims unavailable")
        with self.assertRaises(LookupError):
            self.portal.dashboard("CL-1")
