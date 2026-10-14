"""Canonical adapter for IMA's Universal Conversation & Interaction Memory.

The adapter is intentionally explicit: callers must provide the user scope,
source, original content and current consent state. It delegates persistence
to the canonical memory runtime instead of maintaining a second store.
"""
from __future__ import annotations

from typing import Any, Mapping

from .memory.universal_interaction_memory import capture, get_consent


def save_memory(memory: Mapping[str, Any]) -> dict:
    """Persist one authorized interaction through the canonical memory runtime.

    Required keys: user_id, source, content, consent.
    Optional keys mirror universal_interaction_memory.capture().
    """
    required = ("user_id", "source", "content", "consent")
    missing = [key for key in required if key not in memory]
    if missing:
        raise ValueError("missing required memory fields: " + ", ".join(missing))

    user_id = str(memory["user_id"])
    consent = str(memory["consent"])
    stored = get_consent(user_id)["status"]
    if stored != consent:
        raise ValueError(
            f"memory consent mismatch: supplied={consent}, stored={stored}"
        )

    allowed = {
        "user_id", "source", "content", "consent", "language", "interface",
        "participants", "translation_refs", "actions", "outcome",
        "verification", "uncertainty", "temporal_class", "evidence_refs",
        "authorized_learning", "status",
    }
    payload = {key: memory[key] for key in allowed if key in memory}
    return capture(**payload)
