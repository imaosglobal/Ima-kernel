"""Canonical context index for IMA's unified conversation surface.

This is an index, not a duplicate memory store. It tells the master runtime which
canonical contracts, capabilities and lifecycle rules belong to the same IMA system.
Private user memory remains in the canonical per-user memory store.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / ".ima" / "CANONICAL_CONTEXT_INDEX.json"

def load_index():
    try:
        return json.loads(INDEX.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _read(path, limit=2400):
    try:
        p = ROOT / path
        if not p.exists(): return ""
        text = p.read_text(encoding="utf-8")
        return text[:limit]
    except Exception:
        return ""

def build_context(message="", language=""):
    index = load_index()
    msg = str(message or "").casefold()
    domains = index.get("domains", [])
    selected = []
    for item in domains:
        terms = [str(x).casefold() for x in item.get("keywords", [])]
        if not terms or any(t in msg for t in terms):
            selected.append(item)
    # These are mandatory cross-cutting sources for every live IMA conversation.
    mandatory_ids = {"roles-professions-human-ai", "verification-self-repair", "human-survival-resilience"}
    for item in domains:
        if item.get("id") in mandatory_ids and item not in selected:
            selected.append(item)
    if not selected:
        selected = domains[:6]
    rows=[]
    for item in selected[:12]:
        summary = str(item.get("summary","")).strip()
        path = str(item.get("path","")).strip()
        excerpt = _read(path, 900) if path else ""
        rows.append(f"- {item.get('id','unknown')}: {summary}" + (f" | canonical source: {path}" if path else "") + (f" | verified excerpt: {excerpt[:900]}" if excerpt else ""))
    return (
        "[IMA canonical unified context — use the same system across IMA chat, "
        "authorized adapters and future hosts. Organize relevant knowledge by "
        "current need, time horizon and generation; do not duplicate authorities. "
        "Private memory is user-scoped and consent-gated.]
"
        + ("Language: " + language + "\n" if language else "")
        + "\n".join(rows)
    )
