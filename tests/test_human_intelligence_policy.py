import unittest

from core.human_intelligence import POLICY_VERSION, SYSTEM_POLICY, compose_prompt


class HumanIntelligencePolicyTests(unittest.TestCase):
    def test_policy_has_version_and_core_purpose(self):
        self.assertTrue(POLICY_VERSION)
        self.assertIn("help humanity", SYSTEM_POLICY)
        self.assertIn("compassion with truth", SYSTEM_POLICY)

    def test_policy_preserves_human_agency_and_relationships(self):
        self.assertIn("cultivate dependence", SYSTEM_POLICY)
        self.assertIn("replacement for human relationships", SYSTEM_POLICY)

    def test_policy_requires_consent_for_cross_user_learning(self):
        self.assertIn("explicit authorization", SYSTEM_POLICY)
        self.assertIn("privacy-preserving", SYSTEM_POLICY)

    def test_prompt_includes_policy_and_user_request(self):
        prompt = compose_prompt("Help me understand a conflict.")
        self.assertIn(SYSTEM_POLICY, prompt)
        self.assertIn("Help me understand a conflict.", prompt)
        self.assertTrue(POLICY_VERSION)

    def test_empty_message_is_handled(self):
        self.assertIn("USER MESSAGE", compose_prompt(""))


if __name__ == "__main__":
    unittest.main()
