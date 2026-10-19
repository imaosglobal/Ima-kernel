import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class TestMonetizationReadiness(unittest.TestCase):
    def test_audit_is_evidence_only_and_blocks_unverified_routes(self):
        p = subprocess.run(
            [sys.executable, "scripts/ima_monetization_readiness.py"],
            cwd=ROOT, text=True, capture_output=True
        )
        self.assertEqual(p.returncode, 0, p.stderr)
        data = json.loads(p.stdout)
        self.assertFalse(data["actual_revenue_claimed"])
        self.assertEqual(data["actual_revenue"], 0)
        self.assertFalse(data["autonomous_spending"])
        self.assertIn("STRIPE_LIVE_NOT_VERIFIED", data["blockers"])
        self.assertIn("COMMERCE_PIPELINE_EMPTY", data["blockers"])

if __name__ == "__main__":
    unittest.main()
