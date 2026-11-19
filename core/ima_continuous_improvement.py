"""Canonical runtime view of IMA's continuous improvement contract."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / ".ima" / "CANONICAL_DOMAIN_AUDIT.json"
CONTRACT_PATH = ROOT / ".ima" / "CONTINUOUS_IMPROVEMENT_MAP.json"

def load_contract() -> dict:
    try:
        data = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}

def build_context(message: str = "") -> str:
    contract = load_contract()
    if not contract:
        return "[IMA improvement loop unavailable: preserve verification, safety and human agency.]"
    return (
        "[IMA continuous improvement loop — same canonical system, no parallel system]\n"
        f"Domain families: {', '.join(contract.get('existing_domain_families', []))}\n"
        f"Lifecycle: {' → '.join(contract.get('lifecycle', []))}\n"
        f"Rules: {'; '.join(contract.get('rules', []))}\n"
        "For this interaction: identify the current need first; reuse existing capabilities; "
        "locate missing evidence or capability; research when needed; separate verified fact "
        "from inference and unknown; then prefer the smallest safe improvement that increases "
        "usefulness, accessibility, reliability or human agency."
    )

def status() -> dict:
    contract = load_contract()
    return {
        "id": contract.get("id"),
        "version": contract.get("version"),
        "status": contract.get("status"),
        "domain_family_count": len(contract.get("existing_domain_families", [])),
        "lifecycle": contract.get("lifecycle", []),
    }


def domain_audit() -> dict:
    try:
        data = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {}
        domains = data.get("domains", [])
        counts = {}
        for item in domains:
            state = item.get("state", "UNKNOWN")
            counts[state] = counts.get(state, 0) + 1
        return {"id": data.get("id"), "version": data.get("version"), "domain_count": len(domains), "evidence_counts": counts, "priority_order": data.get("priority_order", [])}
    except Exception:
        return {}
