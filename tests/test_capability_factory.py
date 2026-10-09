import unittest
from datetime import datetime, timezone
from pathlib import Path
import importlib.util

MODULE_PATH = Path(__file__).resolve().parents[1] / ".ima" / "plugins" / "capability_factory.py"
spec = importlib.util.spec_from_file_location("ima_capability_factory_test", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
CapabilityAdapter = module.CapabilityAdapter
CapabilityEvidence = module.CapabilityEvidence
CapabilityGap = module.CapabilityGap
verify_adapter = module.verify_adapter
GAP_STATES = module.GAP_STATES


class CapabilityFactoryTests(unittest.TestCase):
    def test_evidence_rejects_unknown_state(self):
        with self.assertRaises(ValueError):
            CapabilityEvidence("imagined", "unit-test", "detail", "2026-10-09T00:00:00Z")

    def test_evidence_requires_source_detail_and_timestamp(self):
        for values in [
            ("tested", "", "detail", "2026-10-09T00:00:00Z"),
            ("tested", "unit-test", "", "2026-10-09T00:00:00Z"),
            ("tested", "unit-test", "detail", ""),
        ]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                CapabilityEvidence(*values)

    def test_adapter_is_not_verified_until_verified_evidence_exists(self):
        adapter = CapabilityAdapter("example", "unit", ["read"])
        self.assertFalse(adapter.is_verified())
        adapter.record(CapabilityEvidence("tested", "unit-test", "test passed", "2026-10-09T00:00:00Z"))
        self.assertFalse(adapter.is_verified())
        adapter.record(CapabilityEvidence("verified", "unit-test", "verified independently", "2026-10-09T00:01:00Z"))
        self.assertTrue(adapter.is_verified())
        self.assertTrue(adapter.health()["verified"])

    def test_gap_cannot_move_backwards_or_to_unknown_state(self):
        gap = CapabilityGap("gap-1", "human_understanding", "Need measurable evaluation")
        gap.advance("specified")
        self.assertEqual(gap.state, "specified")
        with self.assertRaises(ValueError):
            gap.advance("detected")
        with self.assertRaises(ValueError):
            gap.advance("imagined")

    def test_verify_adapter_records_test_and_verification_only_on_success(self):
        adapter = CapabilityAdapter("example", "unit", ["read"])
        result = verify_adapter(adapter, lambda: True, "unit-test", "2026-10-09T00:00:00Z")
        self.assertTrue(result)
        self.assertTrue(adapter.is_verified())
        self.assertEqual([item.state for item in adapter.evidence], ["tested", "verified"])

    def test_false_test_is_not_verified(self):
        adapter = CapabilityAdapter("example", "unit", ["read"])
        result = verify_adapter(adapter, lambda: False, "unit-test", "2026-10-09T00:00:00Z")
        self.assertFalse(result)
        self.assertFalse(adapter.is_verified())
        self.assertEqual([item.state for item in adapter.evidence], ["tested"])


if __name__ == "__main__":
    unittest.main()
