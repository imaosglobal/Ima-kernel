"""Canonical adapters for useful legacy IMA capability semantics.

Legacy repositories remain provenance sources. This module ports only behavior that
can be expressed safely inside the canonical learning/action boundary. It does not
create a second brain, memory store, feedback store, or autonomous executor.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

Intent = Literal["chat", "commerce", "learning", "memory_request"]

@dataclass(frozen=True)
class LegacyIntent:
    intent: Intent
    requested_actions: tuple[str, ...]

def classify_legacy_intent(text: str) -> LegacyIntent:
    """Translate useful legacy intent semantics into canonical data.

    No action is executed here. Consequential actions must pass the canonical
    consent/action gate.
    """
    value = (text or "").strip().lower()
    actions: list[str] = []
    intent: Intent = "chat"

    if any(token in value for token in ("קנה", "מוצר", "חנות", "buy", "product", "store")):
        intent = "commerce"
        actions.append("open_store")
    if any(token in value for token in ("למד", "ללמוד", "לימוד", "learn", "learning")):
        intent = "learning"
        actions.append("activate_learning")
    if any(token in value for token in ("זכור", "שמור בזיכרון", "remember", "save memory")):
        intent = "memory_request"
        actions.append("store_memory")
    return LegacyIntent(intent=intent, requested_actions=tuple(actions))

def action_requires_confirmation(action: str) -> bool:
    return action in {"open_store", "store_memory", "activate_learning"}
