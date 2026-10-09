import unittest

from learning.learning_gate import should_learn


class LearningGateTests(unittest.TestCase):
    def test_user_content_is_denied_without_explicit_authorization(self):
        self.assertFalse(should_learn({"source": "user", "text": "A meaningful personal story"}))
        self.assertFalse(should_learn({"text": "A meaningful personal story"}))

    def test_user_content_can_pass_only_with_explicit_authorization(self):
        self.assertTrue(should_learn({
            "source": "user",
            "text": "A contribution approved for shared learning",
            "learning_authorized": True,
        }))

    def test_private_content_is_never_eligible(self):
        self.assertFalse(should_learn({
            "source": "user",
            "text": "A contribution approved for shared learning",
            "learning_authorized": True,
            "privacy_class": "private",
        }))

    def test_revoked_consent_blocks_learning(self):
        self.assertFalse(should_learn({
            "source": "user",
            "text": "A contribution approved for shared learning",
            "learning_authorized": True,
            "consent_revoked": True,
        }))

    def test_system_learning_is_not_blocked_by_user_consent_rule(self):
        self.assertTrue(should_learn({"source": "ima", "text": "A sufficiently long system learning event"}))

    def test_short_and_internal_loop_events_are_ignored(self):
        self.assertFalse(should_learn({"source": "ima", "text": "short"}))
        self.assertFalse(should_learn({"source": "ima", "text": "דפוסים חוזרים מהשיחה"}))


if __name__ == "__main__":
    unittest.main()
