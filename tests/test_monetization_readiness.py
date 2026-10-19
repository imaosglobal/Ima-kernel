import json, subprocess, sys, unittest
class TestMonetizationReadiness(unittest.TestCase):
    def test_paypal_primary_and_no_unverified_income(self):
        p=subprocess.run([sys.executable,"scripts/ima_monetization_readiness.py"],text=True,capture_output=True)
        self.assertEqual(p.returncode,0,p.stderr)
        d=json.loads(p.stdout)
        self.assertEqual(d["primary_payment_provider"],"paypal")
        self.assertFalse(d["actual_revenue_claimed"])
        self.assertEqual(d["actual_revenue"],0)
        self.assertFalse(d["autonomous_spending"])
        self.assertIn("PAYPAL_LIVE_ACCOUNT_NOT_VERIFIED",d["blockers"])
