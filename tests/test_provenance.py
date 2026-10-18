import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class TestProvenance(unittest.TestCase):
    def test_canonical_provenance_record_exists(self):
        p = ROOT / "docs" / "IMA_FIRST_PRIORITY_PROVENANCE.md"
        self.assertTrue(p.exists())
        text = p.read_text(encoding="utf-8")
        self.assertIn("Ori Cohen", text)
        self.assertIn("human imagination -> technological possibility", text)
        self.assertIn("IMAGINED -> PROPOSED -> IMPLEMENTED -> TESTED -> DEPLOYED -> VERIFIED_LIVE", text)

    def test_unified_loop_contains_global_reconciliation_rules(self):
        p = ROOT / ".ima" / "loop" / "unified_loop.py"
        text = p.read_text(encoding="utf-8")
        self.assertIn("first-priority provenance", text)
        self.assertIn("cross-domain reconciliation", text)
        self.assertIn("global user benefit", text)
        self.assertIn('"provenance_rule"', text)
        self.assertIn('"cross_domain_reconciliation_rule"', text)

if __name__ == "__main__":
    unittest.main()
