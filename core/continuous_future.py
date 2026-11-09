"""Canonical cross-component policy for IMA's continuous future lifecycle."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / ".ima" / "policies" / "CONTINUOUS_FUTURE_POLICY.json"

def load_policy() -> dict:
    try:
        data = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}

def policy_context() -> str:
    p = load_policy()
    if not p:
        return "IMA continuous-future policy unavailable: treat future as unknown and preserve verification, safety and human agency."
    return (
        "IMA-CONTINUOUS-FUTURE-001 | "
        f"principle={p.get('principle','')} | "
        f"lifecycle={' -> '.join(p.get('lifecycle', []))} | "
        "all_components=shared_policy | "
        "boundary=human/platform/legal authority remains controlling"
    )

def component_contract(component: str) -> dict:
    p = load_policy()
    return {
        "component": component,
        "policy_id": p.get("id", "IMA-CONTINUOUS-FUTURE-001"),
        "principle": p.get("principle", ""),
        "lifecycle": p.get("lifecycle", []),
        "always_apply": p.get("always_apply", []),
        "boundary": p.get("boundary", ""),
        "shared_with": "all IMA components",
    }
