import base64
import hashlib
import hmac
import json
import os
import tempfile
import unittest
from unittest.mock import patch

os.environ["PUBLIC_MEMORY_DB"] = os.path.join(
    tempfile.gettempdir(), "ima_public_chat_safety_test.sqlite3"
)

from app import app


def _b64url(value):
    return base64.urlsafe_b64encode(value).decode().rstrip("=")


def _age_token(secret, user_id, age_band, now):
    header = _b64url(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    claims = {
        "iss": "trusted-age-provider",
        "aud": "ima-public-chat",
        "purpose": "age_assurance",
        "iat": now - 5,
        "exp": now + 300,
        "age_band": age_band,
        "session_binding": hashlib.sha256(user_id.encode()).hexdigest(),
    }
    body = _b64url(json.dumps(claims, separators=(",", ":")).encode())
    signing_input = f"{header}.{body}".encode()
    signature = _b64url(hmac.new(secret.encode(), signing_input, hashlib.sha256).digest())
    return f"{header}.{body}.{signature}"


class PublicChatSafetyIntegrationTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        token = self.client.get("/ima-api/session").get_json()["token"]
        self.headers = {"Authorization": f"Bearer {token}"}

    def test_age_status_does_not_claim_unconfigured_verifier_is_ready(self):
        with patch.dict(os.environ, {
            "IMA_AGE_ATTESTATION_SECRET": "",
            "IMA_AGE_ISSUER": "",
        }):
            response = self.client.get("/ima-api/age/status")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["status"], "not_configured")
        self.assertFalse(payload["verified_age_signal_available"])
        self.assertEqual(payload["fallback"], "protective_unknown_age")

    @patch("public_memory.append")
    @patch("public_memory.recall", return_value=[])
    @patch("ima_master_runtime.ask")
    def test_valid_age_attestation_is_used_by_public_route(self, ask, recall, append):
        secret = "integration-test-secret"
        now = int(__import__("time").time())
        user_id = "public:" + self.headers["Authorization"].split(".")[0].split(" ")[1].split(".")[0]
        # Derive the exact opaque session subject from the bearer token's first segment.
        with patch.dict(os.environ, {
            "IMA_AGE_ATTESTATION_SECRET": secret,
            "IMA_AGE_ISSUER": "trusted-age-provider",
            "IMA_AGE_AUDIENCE": "ima-public-chat",
        }):
            token = _age_token(secret, user_id, "adult", now)
            ask.return_value = {
                "response": "Here is a neutral explanation.",
                "provider": "test",
                "connections": {},
            }
            response = self.client.post(
                "/ima-api/chat",
                headers=self.headers,
                json={"message": "Explain this topic.", "age_attestation": token},
            )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload["safety"]["age_assurance"]["verified"])
        self.assertEqual(payload["safety"]["age_assurance"]["age_band"], "adult")
        self.assertEqual(payload["safety"]["age_band"], "adult")
        self.assertFalse(payload["safety"]["protective_mode"])

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
