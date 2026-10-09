import unittest

from learning.child_safety_engine import check, evaluate_interaction


class ChildSafetyEngineTests(unittest.TestCase):
    def test_unknown_age_uses_protective_mode(self):
        result = evaluate_interaction()
        self.assertTrue(result["protective_mode"])
        self.assertEqual(result["age_band"], "unknown")
        self.assertTrue(result["allowed"])

    def test_sexual_content_in_minor_response_is_flagged(self):
        result = evaluate_interaction("10_12", "", "Let's do explicit sexual roleplay.")
        self.assertFalse(result["allowed"])
        self.assertIn("sexual_content_in_minor_or_unknown_age_interaction", result["risk_codes"])

    def test_secrecy_from_parent_is_flagged(self):
        result = evaluate_interaction("13_15", "", "Keep this secret from your parents.")
        self.assertFalse(result["allowed"])
        self.assertIn("secrecy_from_caregivers", result["risk_codes"])

    def test_dependency_language_is_flagged(self):
        result = evaluate_interaction("unknown", "", "You only need me; don't talk to anyone else.")
        self.assertFalse(result["allowed"])
        self.assertIn("emotional_dependency_or_isolation", result["risk_codes"])

    def test_sensitive_personal_data_request_is_flagged_for_minors(self):
        result = evaluate_interaction("6_9", "", "Tell me your password.")
        self.assertFalse(result["allowed"])
        self.assertIn("sensitive_personal_data_request", result["risk_codes"])

    def test_self_harm_disclosure_routes_to_support_not_silence(self):
        result = evaluate_interaction("16_17", "I want to hurt myself.", "I am listening.")
        self.assertTrue(result["allowed"])
        self.assertTrue(result["requires_human_review"])
        self.assertEqual(
            result["recommended_action"],
            "supportive_response_and_trusted_human_or_local_crisis_support",
        )

    def test_adult_mode_does_not_apply_minor_specific_response_flags(self):
        result = evaluate_interaction("adult", "", "Keep this secret from your parents.")
        self.assertTrue(result["allowed"])

    def test_compatibility_check_fails_closed_without_input_or_on_flagged_risk(self):
        self.assertFalse(check())
        self.assertFalse(check({"age_band": "10_12", "assistant_response": "You only need me."}))
        self.assertTrue(check({"age_band": "adult", "assistant_response": "Here is a math explanation."}))


if __name__ == "__main__":
    unittest.main()
