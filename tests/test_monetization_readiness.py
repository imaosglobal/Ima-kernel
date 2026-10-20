import json, subprocess, sys
import unittest

class TestMonetizationReadiness(unittest.TestCase):
    def test_multi_provider_router_and_no_unverified_income(self):
        p = subprocess.run(
            [sys.executable, "scripts/ima_monetization_readiness.py"],
            text=True, capture_output=True
        )
        self.assertEqual(p.returncode, 0, p.stderr)
        d = json.loads(p.stdout)
        self.assertEqual(d["payment_router_mode"], "multi_provider_router")
        self.assertEqual(d["primary_payment_provider"], "paypal")
        for provider in ["paypal", "google_pay", "apple_pay", "github_sponsors", "youtube", "open_collective", "future_provider"]:
            self.assertIn(provider, d["providers"])
        self.assertFalse(d["actual_revenue_claimed"])
        self.assertEqual(d["actual_revenue"], 0)
        self.assertFalse(d["autonomous_spending"])
        self.assertEqual(d["blockers"], [])
