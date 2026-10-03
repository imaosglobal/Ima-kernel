import os
import tempfile
import unittest

os.environ["PUBLIC_MEMORY_DB"] = os.path.join(
    tempfile.gettempdir(), "ima_public_memory_test.sqlite3"
)

from app import app
import public_memory


class PublicRuntimeContractTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.user_a = "test-user-a"
        self.user_b = "test-user-b"

    def _session_headers(self):
        token = self.client.get("/ima-api/session").get_json()["token"]
        return {"Authorization": f"Bearer {token}"}

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get("status"), "ok")

    def test_runtime_contract_reports_private_boundary(self):
        response = self.client.get("/ima-api/runtime")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["memory"]["mode"], "per-user")
        self.assertFalse(payload["memory"]["private_founder_memory_exposed"])
        self.assertTrue(payload["capabilities"]["per_user_session_memory"])
        self.assertFalse(payload["capabilities"]["autonomous_external_actions"])

    def test_memory_isolation(self):
        public_memory.append(self.user_a, "secret-a", "answer-a")
        public_memory.append(self.user_b, "secret-b", "answer-b")
        self.assertTrue(public_memory.recent(self.user_a))
        self.assertTrue(public_memory.recent(self.user_b))
        self.assertEqual(public_memory.recall(self.user_a, "secret-b"), [])
        self.assertEqual(public_memory.recall(self.user_b, "secret-a"), [])

    def test_empty_chat_is_rejected(self):
        response = self.client.post(
            "/ima-api/chat",
            headers={"X-IMA-User": self.user_a},
            json={"message": ""}
        )
        self.assertEqual(response.status_code, 400)


    def test_chat_rejects_unsigned_identity_headers(self):
        response = self.client.post(
            "/ima-api/chat",
            headers={"X-IMA-User": self.user_a},
            json={"message": "What is IMA?"}
        )
        self.assertEqual(response.status_code, 401)

    def test_session_tokens_are_signed(self):
        token = self.client.get("/ima-api/session").get_json()["token"]
        forged = token.rsplit(".", 1)[0] + ".invalid"
        response = self.client.post(
            "/ima-api/chat",
            headers={"Authorization": f"Bearer {forged}"},
            json={"message": "What is IMA?"}
        )
        self.assertEqual(response.status_code, 401)

    def test_chat_contract_and_user_scope(self):
        response = self.client.post(
            "/ima-api/chat",
            headers=self._session_headers(),
            json={"message": "What is IMA?"}
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("response", payload)
        self.assertEqual(payload["memory"]["scope"], "user")
        self.assertTrue(payload["verified"])

if __name__ == "__main__":
    unittest.main()
