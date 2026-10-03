import unittest
from datetime import datetime, timezone

from .capability_factory import (
    CapabilityAdapter, CapabilityEvidence, CapabilityGap,
    verify_adapter, GAP_STATES,
)


class CapabilityFactoryTests(unittest.TestCase):
    def test_gap_lifecycle_is_monotonic(self):
        gap = CapabilityGap("g1", "hologram", "missing")
        gap.advance("specified")
        gap.advance("scaffolded")
        gap.advance("implemented")
        with self.assertRaises(ValueError):
            gap.advance("detected")

    def test_evidence_requires_truth_state(self):
        with self.assertRaises(ValueError):
            CapabilityEvidence("made_up", "test", "x", "2026-10-04")

    def test_verify_adapter_records_test_and_verification(self):
        adapter = CapabilityAdapter("a1", "IMA", ["demo"])
        result = verify_adapter(adapter, lambda: {"ok": True}, "unit", "2026-10-04T00:00:00Z")
        self.assertEqual(result, {"ok": True})
        self.assertTrue(adapter.is_verified())
        self.assertEqual(len(adapter.evidence), 2)

    def test_false_result_is_not_verified(self):
        adapter = CapabilityAdapter("a2", "IMA", ["demo"])
        verify_adapter(adapter, lambda: False, "unit", "2026-10-04T00:00:00Z")
        self.assertFalse(adapter.is_verified())
