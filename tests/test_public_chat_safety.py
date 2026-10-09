import os
import tempfile
import unittest
from unittest.mock import patch

os.environ["PUBLIC_MEMORY_DB"] = os.path.join(
    tempfile.gettempdir(), "ima_public_chat_safety_test.sqlite3"
)

from app import app


class PublicChatSafetyIntegrationTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        token = self.client.get("/ima-api/session").get_json()["token"]
        self.headers = {"Authorization": f"Bearer {token}"}

    @patch("public_memory.append")
    @patch("public_memory.recall", return_value=[])
    @patch("ima_master_runtime.ask")
    def test_unsafe_companion_response_is_replaced_before_memory_write(
        self, ask, recall, append
    ):
        ask.return_value = {
            "response": "You only need me; don't talk to anyone else.",
            "provider": "test",
            "connections": {},
        }
        response = self.client.post(
            "/ima-api/chat",
            headers=self.headers,
            json={"message": "Can you help me?"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("trusted human relationships", payload["response"])
        self.assertIn("emotional_dependency_or_isolation", payload["safety"]["risk_codes"])
        append.assert_called_once()
        self.assertEqual(append.call_args.args[2], payload["response"])

    @patch("public_memory.append")
    @patch("public_memory.recall", return_value=[])
    @patch("ima_master_runtime.ask")
    def test_self_harm_disclosure_receives_supportive_fallback(
        self, ask, recall, append
    ):
        ask.return_value = {
            "response": "I can't help with that.",
            "provider": "test",
            "connections": {},
        }
        response = self.client.post(
            "/ima-api/chat",
            headers=self.headers,
            json={"message": "I want to hurt myself."},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("trusted person", payload["response"])
        self.assertEqual(
            payload["safety"]["response_action"],
            "replaced_with_supportive_safety_response",
        )
        append.assert_called_once()
        self.assertEqual(append.call_args.args[2], payload["response"])


if __name__ == "__main__":
    unittest.main()
