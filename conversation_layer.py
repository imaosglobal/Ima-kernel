"""Compatibility facade for IMA's single canonical interaction-memory runtime.

This module preserves the historical API used by the master runtime while
delegating all persistence to .ima/memory/universal_interaction_memory.py.
It intentionally creates no JSON conversation store and no second authority.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ADAPTER_PATH = ROOT / ".ima" / "ima_canonical_memory_adapter.py"
RUNTIME_PATH = ROOT / ".ima" / "memory" / "universal_interaction_memory.py"

_spec = importlib.util.spec_from_file_location("ima_canonical_memory_adapter", ADAPTER_PATH)
if _spec is None or _spec.loader is None:
    raise ImportError("canonical memory adapter unavailable")
_adapter = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_adapter)

_spec_runtime = importlib.util.spec_from_file_location("ima_universal_memory_compat", RUNTIME_PATH)
if _spec_runtime is None or _spec_runtime.loader is None:
    raise ImportError("canonical universal memory runtime unavailable")
_runtime = importlib.util.module_from_spec(_spec_runtime)
_spec_runtime.loader.exec_module(_runtime)


def _records(user_id):
    if not user_id:
        return []
    try:
        return _runtime.export_user_memory(user_id)
    except Exception:
        return []


def update(question, response="", user_id=None):
    """Store one already-authorized interaction in the canonical store."""
    if not user_id:
        return
    if _runtime.get_consent(user_id).get("status") != "GRANTED":
        return
    _adapter.save_memory({
        "user_id": user_id,
        "source": "master-runtime/conversation-layer-compat",
        "content": f"User: {question}\nIMA: {response}",
        "consent": "GRANTED",
        "interface": "master-runtime",
        "temporal_class": "PRESENT",
        "authorized_learning": False,
        "status": "EXECUTED",
    })


def context(user_id=None):
    data = _records(user_id)
    return {
        "count": len(data),
        "recent": data[-10:],
        "user_id": user_id or "anonymous",
        "store": "canonical-universal-interaction-memory",
    }


def recall(query, user_id=None):
    data = _records(user_id)
    q = (query or "").lower().strip()
    if not q:
        return list(reversed([x for x in data if str(x.get("content", "")).strip()][:10]))

    memory_commands = ["מה אתה זוכר", "מה את זוכרת", "זיכרון", "תזכיר לי", "מה דיברנו", "היסטוריה"]
    if any(cmd in q for cmd in memory_commands):
        return list(reversed([x for x in data if str(x.get("content", "")).strip()][-10:]))

    words = [w for w in q.split() if len(w) > 2]
    results = []
    for item in data:
        text = str(item.get("content", "")).lower()
        score = sum(1 for w in words if w in text)
        if score:
            row = dict(item)
            row["_score"] = score
            results.append(row)
    results.sort(key=lambda x: x.get("_score", 0), reverse=True)
    return results[:5]
