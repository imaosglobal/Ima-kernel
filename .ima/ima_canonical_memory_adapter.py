"""Canonical adapter for IMA's Universal Conversation & Interaction Memory.

This adapter delegates to the single canonical runtime and creates no parallel
memory store.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any, Mapping

_ROOT = Path(__file__).resolve().parent
_RUNTIME = _ROOT / "memory" / "universal_interaction_memory.py"
_SPEC = importlib.util.spec_from_file_location("ima_universal_interaction_memory", _RUNTIME)
if not _SPEC or not _SPEC.loader:
    raise ImportError("canonical universal interaction memory runtime is unavailable")
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)

capture = _MODULE.capture
get_consent = _MODULE.get_consent


def save_memory(memory: Mapping[str, Any]) -> dict:
    """Persist one interaction through the canonical memory runtime."""
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
    return capture(**{key: memory[key] for key in allowed if key in memory})
