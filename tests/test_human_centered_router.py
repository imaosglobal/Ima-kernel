import unittest

from core.conversation_router import route


class HumanCenteredRouterTests(unittest.TestCase):
    def test_greeting_does_not_hardcode_a_person_name(self):
        response = route("שלום")
        self.assertIn("אני אמא", response)
        self.assertNotIn("אורי", response)

    def test_identity_is_human_centered_without_claiming_human_status(self):
        response = route("מי את")
        self.assertIn("בינה אנושית", response)
        self.assertIn("אני לא אדם", response)
        self.assertIn("בחירה האנושית", response)

    def test_status_question_does_not_claim_unverified_runtime_health(self):
        response = route("מה נשמע")
        self.assertNotIn("הליבה פעילה", response)
        self.assertIn("מה חשוב לך", response)

    def test_unrecognized_question_is_delegated(self):
        self.assertIsNone(route("איך מתקנים את המחשב שלי?"))


if __name__ == "__main__":
    unittest.main()
