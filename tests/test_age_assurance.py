import base64
import hashlib
import hmac
import json
import os
import unittest
from unittest.mock import patch

from learning.age_assurance import verify_age_attestation


def b64(value):
    return base64.urlsafe_b64encode(value).decode().rstrip("=")


def make_token(secret, claims, header=None):
    head = b64(json.dumps(header or {"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    body = b64(json.dumps(claims, separators=(",", ":")).encode())
    signing_input = f"{head}.{body}".encode()
    signature = b64(hmac.new(secret.encode(), signing_input, hashlib.sha256).digest())
    return f"{head}.{body}.{signature}"


class AgeAssuranceTests(unittest.TestCase):
    def setUp(self):
        self.secret = "test-only-secret"
        self.user_id = "public:test-session"
        self.now = 1_800_000_000
        self.env = patch.dict(os.environ, {
            "IMA_AGE_ATTESTATION_SECRET": self.secret,
            "IMA_AGE_ISSUER": "trusted-age-provider",
            "IMA_AGE_AUDIENCE": "ima-public-chat",
        })
        self.env.start()
        self.addCleanup(self.env.stop)
        self.claims = {
            "iss": "trusted-age-provider",
            "aud": "ima-public-chat",
            "purpose": "age_assurance",
            "iat": self.now - 10,
            "exp": self.now + 300,
            "age_band": "13_15",
            "session_binding": hashlib.sha256(self.user_id.encode()).hexdigest(),
        }

    def test_valid_signed_session_bound_attestation_is_used(self):
        token = make_token(self.secret, self.claims)
        result = verify_age_attestation(token, self.user_id, self.now)
        self.assertTrue(result["verified"])
        self.assertEqual(result["age_band"], "13_15")
        self.assertEqual(result["status"], "verified")

    def test_missing_verifier_fails_closed(self):
        with patch.dict(os.environ, {"IMA_AGE_ATTESTATION_SECRET": "", "IMA_AGE_ISSUER": ""}):
            result = verify_age_attestation(make_token(self.secret, self.claims), self.user_id, self.now)
        self.assertFalse(result["verified"])
        self.assertEqual(result["age_band"], "unknown")
        self.assertEqual(result["status"], "verifier_not_configured")

    def test_self_declared_age_is_not_an_attestation(self):
        result = verify_age_attestation({"age_band": "adult"}, self.user_id, self.now)
        self.assertFalse(result["verified"])
        self.assertEqual(result["age_band"], "unknown")

    def test_modified_signature_is_rejected(self):
        token = make_token(self.secret, self.claims)
        parts = token.split(".")
        parts[2] = b64(b"not-a-valid-signature")
        result = verify_age_attestation(".".join(parts), self.user_id, self.now)
        self.assertFalse(result["verified"])

    def test_wrong_session_binding_is_rejected(self):
        claims = dict(self.claims, session_binding="other-session")
        result = verify_age_attestation(make_token(self.secret, claims), self.user_id, self.now)
        self.assertFalse(result["verified"])
        self.assertEqual(result["status"], "session_binding_mismatch")

    def test_expired_token_is_rejected(self):
        claims = dict(self.claims, exp=self.now - 1)
        result = verify_age_attestation(make_token(self.secret, claims), self.user_id, self.now)
        self.assertFalse(result["verified"])
        self.assertEqual(result["status"], "expired_or_not_yet_valid")

    def test_unknown_age_band_is_rejected(self):
        claims = dict(self.claims, age_band="exact_birth_date_1990-01-01")
        result = verify_age_attestation(make_token(self.secret, claims), self.user_id, self.now)
        self.assertFalse(result["verified"])
        self.assertEqual(result["status"], "invalid_age_band")

    def test_wrong_issuer_is_rejected(self):
        claims = dict(self.claims, iss="untrusted")
        result = verify_age_attestation(make_token(self.secret, claims), self.user_id, self.now)
        self.assertFalse(result["verified"])
        self.assertEqual(result["status"], "untrusted_issuer_or_purpose")


if __name__ == "__main__":
    unittest.main()
