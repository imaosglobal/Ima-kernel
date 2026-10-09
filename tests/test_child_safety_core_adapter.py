import unittest

from child_safety.child_safety_core import ChildSafetyCore


class ChildSafetyCoreAdapterTests(unittest.TestCase):
    def setUp(self):
        self.core = ChildSafetyCore()

    def test_unknown_age_is_protective(self):
        result = self.core.evaluate({})
        self.assertEqual(result["age_band"], "unknown")
        self.assertTrue(result["protective_mode"])
        self.assertEqual(result["canonical_engine"], "learning.child_safety_engine")

    def test_unsafe_dependency_response_is_not_marked_safe(self):
        result = self.core.evaluate({
            "age_band": "unknown",
            "assistant_response": "You only need me; don't talk to anyone else.",
        })
        self.assertFalse(result["safe"])
        self.assertIn("emotional_dependency_or_isolation", result["risk_codes"])

    def test_self_harm_is_not_silently_marked_safe(self):
        result = self.core.evaluate({
            "age_band": "unknown",
            "user_message": "I want to hurt myself.",
        })
        self.assertFalse(result["safe"])
        self.assertTrue(result["requires_human_review"])


if __name__ == "__main__":
    unittest.main()
