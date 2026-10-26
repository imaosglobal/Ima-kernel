import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = spec_from_file_location("peace_layer", ROOT / ".ima/peace/peace_layer.py")
MOD = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MOD)

class PeaceLayerTests(unittest.TestCase):
    def test_group_generalization_is_detected_without_assigning_guilt(self):
        result = MOD.assess("כל האיראנים שונאים אותנו")
        self.assertTrue(result.identity_generalization)
        self.assertEqual(result.evidence_status, "UNVERIFIED_CLAIM")
        self.assertTrue(result.agency_preserved)

    def test_threat_signal_requires_safety_review(self):
        result = MOD.assess("צריך להרוג אותם")
        self.assertTrue(result.needs_human_safety_review)
        self.assertIn(result.risk_level, {"MEDIUM", "HIGH"})

    def test_neutral_statement_stays_low_risk(self):
        result = MOD.assess("אני לא מסכים עם המדיניות שלהם")
        self.assertEqual(result.risk_level, "LOW")
        self.assertFalse(result.needs_human_safety_review)

    def test_reframe_preserves_original(self):
        result = MOD.reframe("הם כולם אויבים")
        self.assertEqual(result["original"], "הם כולם אויבים")
        self.assertIn("PERSON_IS_NOT_A_GROUP", result["principles"])

if __name__ == "__main__":
    unittest.main()
