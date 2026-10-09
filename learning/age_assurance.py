"""Privacy-preserving verification of signed, session-bound age attestations.

This module does not estimate age or trust self-declared ages. A configured,
trusted issuer must sign a short-lived HS256 JWT with:
  iss, aud, iat, exp, purpose="age_assurance", age_band, session_binding.
The issuer and IMA must protect/share IMA_AGE_ATTESTATION_SECRET securely.
Only an age band is retained/exposed; exact birth dates and identity data are
neither required nor accepted by this contract.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time
from typing import Any, Dict

AGE_BANDS = {"under_5", "6_9", "10_12", "13_15", "16_17", "adult"}
MAX_TOKEN_LENGTH = 8192
MAX_ATTESTATION_LIFETIME_SECONDS = 900
CLOCK_SKEW_SECONDS = 60


def _b64url_decode(value: str) -> bytes:
    if not value or not isinstance(value, str):
        raise ValueError("empty base64url segment")
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _unknown(status: str) -> Dict[str, Any]:
    return {"verified": False, "age_band": "unknown", "status": status}


def verify_age_attestation(
    token: Any, session_user_id: str, now: int | None = None
) -> Dict[str, Any]:
    """Verify trusted issuer signature, purpose, audience, time, and session binding."""
    secret = os.environ.get("IMA_AGE_ATTESTATION_SECRET", "")
    issuer = os.environ.get("IMA_AGE_ISSUER", "")
    audience = os.environ.get("IMA_AGE_AUDIENCE", "ima-public-chat")
    if not secret or not issuer:
        return _unknown("verifier_not_configured")
    if not isinstance(token, str) or not token or len(token) > MAX_TOKEN_LENGTH:
        return _unknown("not_provided" if not token else "invalid")
    parts = token.split(".")
    if len(parts) != 3:
        return _unknown("invalid")
    try:
        header = json.loads(_b64url_decode(parts[0]))
        claims = json.loads(_b64url_decode(parts[1]))
        if not isinstance(header, dict) or header.get("alg") != "HS256":
            return _unknown("invalid")
        if header.get("typ") not in (None, "JWT"):
            return _unknown("invalid")
        signing_input = (parts[0] + "." + parts[1]).encode("ascii")
        expected = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
        supplied = _b64url_decode(parts[2])
        if not hmac.compare_digest(expected, supplied):
            return _unknown("invalid")
        if not isinstance(claims, dict):
            return _unknown("invalid")
        current = int(time.time()) if now is None else int(now)
        issued_at = claims.get("iat")
        expires_at = claims.get("exp")
        if claims.get("iss") != issuer or claims.get("purpose") != "age_assurance":
            return _unknown("untrusted_issuer_or_purpose")
        token_audience = claims.get("aud")
        if not (token_audience == audience or
                isinstance(token_audience, list) and audience in token_audience):
            return _unknown("wrong_audience")
        if not isinstance(issued_at, (int, float)) or not isinstance(expires_at, (int, float)):
            return _unknown("missing_time_claims")
        if issued_at > current + CLOCK_SKEW_SECONDS or expires_at <= current:
            return _unknown("expired_or_not_yet_valid")
        if expires_at <= issued_at or expires_at - issued_at > MAX_ATTESTATION_LIFETIME_SECONDS:
            return _unknown("invalid_lifetime")
        if current - issued_at > MAX_ATTESTATION_LIFETIME_SECONDS + CLOCK_SKEW_SECONDS:
            return _unknown("stale")
        age_band = claims.get("age_band")
        if age_band not in AGE_BANDS:
            return _unknown("invalid_age_band")
        expected_binding = hashlib.sha256(str(session_user_id).encode("utf-8")).hexdigest()
        binding = claims.get("session_binding")
        if not isinstance(binding, str) or not hmac.compare_digest(binding, expected_binding):
            return _unknown("session_binding_mismatch")
        return {
            "verified": True,
            "age_band": age_band,
            "status": "verified",
            "issuer": issuer,
            "issued_at": int(issued_at),
            "expires_at": int(expires_at),
        }
    except (ValueError, TypeError, UnicodeError, json.JSONDecodeError, base64.binascii.Error):
        return _unknown("invalid")
