import os
import tempfile
import unittest

os.environ["IMA_PUBLIC_MEMORY_DB"] = os.path.join(tempfile.gettempdir(), "ima_public_memory_test.sqlite3")

from app import app
from public_memory import PublicMemory


class PublicRuntimeContractTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.memory = PublicMemory(os.environ["IMA_PUBLIC_MEMORY_DB"])
        self.user_a = "test-user-a"
        self.user_b = "test-user-b"

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json().get("ok"))

    def test_runtime_contract_reports_private_boundary(self):
        response = self.client.get("/ima-api/runtime")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["memory"]["mode"], "per-user")
        self.assertFalse(payload["memory"]["private_founder_memory_exposed"])

    def test_memory_isolation(self):
        self.memory.append(self.user_a, "secret-a", "answer-a")
        self.memory.append(self.user_b, "secret-b", "answer-b")
        self.assertTrue(self.memory.recent(self.user_a))
        self.assertTrue(self.memory.recent(self.user_b))
        self.assertEqual(self.memory.recall(self.user_a, "secret-b"), [])
        self.assertEqual(self.memory.recall(self.user_b, "secret-a"), [])

    def test_chat_contract_and_user_scope(self):
        response = self.client.post(
            "/ima-api/chat",
            headers={"X-IMA-User": self.user_a},
            json={"message": "What is IMA?"}
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload.get("ok"))
        self.assertIn("response", payload)
        self.assertEqual(payload.get("user_scope"), self.user_a)

    def test_empty_chat_is_rejected(self):
        response = self.client.post(
            "/ima-api/chat",
            headers={"X-IMA-User": self.user_a},
            json={"message": ""}
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
