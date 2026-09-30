"""Convert learned knowledge into testable, bounded application skills.

A learned fact is not treated as a capability until an application path and
verification plan exist. Compilation never executes external actions.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "integrations" / "IMA_SKILL_REGISTRY.json"
STATE_DIR = ROOT / ".ima" / "skills"
STATE_FILE = STATE_DIR / "compiled_skills.jsonl"

DOMAIN_HINTS = {
    "space": ["space", "orbit", "rocket", "satellite", "mars", "moon", "חלל", "מסלול", "לוויין", "מאדים", "ירח"],
    "xr": ["vr", "ar", "mr", "xr", "webxr", "openxr", "מציאות מדומה", "מציאות רבודה"],
    "software": ["software", "api", "sdk", "code", "program", "תוכנה", "קוד", "ממשק"],
    "robotics": ["robot", "robotics", "רובוט", "רובוטיקה"],
    "smart-home": ["matter", "iot", "smart home", "בית חכם"],
    "knowledge": ["research", "science", "study", "מחקר", "מדע", "לימוד"],
}

def _domain(text: str) -> str:
    value = (text or "").lower()
    for domain, hints in DOMAIN_HINTS.items():
        if any(h.lower() in value for h in hints):
            return domain
    return "general"

def _slug(text: str) -> str:
    normalized = re.sub(r"[^a-z0-9א-ת]+", "-", (text or "").lower()).strip("-")
    return normalized[:80] or "general-skill"

def _id(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def compile_skill(event: Dict[str, Any]) -> Dict[str, Any]:
    """Compile a knowledge event into a skill spec without executing it."""
    text = str(event.get("text") or event.get("topic") or "").strip()
    domain = _domain(text)
    skill_key = _id(f"{domain}:{text}")
    now = time.time()
    return {
        "schema": "IMA-APPLIED-SKILL-1.0",
        "skill_id": skill_key,
        "slug": _slug(f"{domain}-{text}"),
        "created_at": now,
        "updated_at": now,
        "source": {
            "event_id": event.get("event_id"),
            "source": event.get("source", "learning"),
            "provenance": event.get("provenance"),
        },
        "knowledge": {
            "domain": domain,
            "statement": text,
            "confidence": event.get("confidence"),
        },
        "application": {
            "intent": "turn_knowledge_into_a_bounded_testable_capability",
            "steps": [
                "define_goal_and_success_criteria",
                "identify_required_tools_and_interfaces",
                "build_or_select_smallest_safe_prototype",
                "run_reproducible_tests",
                "verify_observed_result_against_expected_result",
                "record_limits_failures_and_rollback",
                "promote_only_verified_capabilities",
            ],
            "required_artifacts": [
                "capability_spec",
                "implementation_or_adapter",
                "test_case",
                "verification_evidence",
                "provenance",
                "rollback_or_disable_path",
            ],
        },
        "verification": {
            "status": "DISCOVERED",
            "tests_required": True,
            "external_action_allowed": False,
            "live_claim_allowed": False,
        },
        "evolution": {
            "next": ["SPECIFY", "IMPLEMENT", "TEST", "VERIFY"],
            "upgrade_rule": "replace_only_after_regression_tests_pass",
        },
        "safety": {
            "human_authorization_required_for_consequential_action": True,
            "no_secrets_in_learning_record": True,
            "no_unsolicited_outreach": True,
            "no_identity_or_memory_merge": True,
        },
    }

def persist_skill(skill: Dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with STATE_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(skill, ensure_ascii=False, sort_keys=True) + "\n")

def compile_and_record(event: Dict[str, Any]) -> Dict[str, Any]:
    skill = compile_skill(event)
    if os.getenv("IMA_COMPILE_SKILLS", "1") == "1":
        persist_skill(skill)
    return skill
