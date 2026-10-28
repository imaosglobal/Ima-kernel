import json
import tempfile
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("public_reconciliation", ROOT / "scripts" / "ima_public_reconciliation.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

class PublicReconciliationTest(unittest.TestCase):
    def test_canonical_sources_exist(self):
        self.assertTrue(all(p.exists() for p in MOD.REQUIRED.values()))

    def test_source_reconciliation_does_not_claim_live(self):
        with tempfile.TemporaryDirectory() as td:
            old = MOD.OUT
            MOD.OUT = Path(td) / "state.json"
            try:
                self.assertEqual(MOD.run(), 0)
                data = json.loads(MOD.OUT.read_text(encoding="utf-8"))
                self.assertEqual(data["status"], "SOURCE_RECONCILED")
                self.assertEqual(data["runtime_status"], "NOT_VERIFIED")
                self.assertTrue(data["checks"]["google_identity_flow_present"])
                self.assertTrue(data["checks"]["chat_entry_present"])
                self.assertTrue(data["checks"]["rtl_localization_present"])
            finally:
                MOD.OUT = old

if __name__ == "__main__":
    unittest.main()
