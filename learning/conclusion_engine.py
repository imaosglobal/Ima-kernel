"""Turn verified learning into explicit conclusions and new learning questions."""

from __future__ import annotations
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".ima" / "learning_conclusions"
FILE = STATE / "conclusions.jsonl"

def _id(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]

def conclude(event: Dict[str, Any], evidence_state: str = "UNVERIFIED") -> Dict[str, Any]:
    topic = str(event.get("topic") or event.get("text") or "general").strip()
    conclusion = str(event.get("conclusion") or "").strip()
    remaining = event.get("remaining_questions") or [
        "What remains uncertain?",
        "What evidence could change this conclusion?",
        "What should be tested or taught next?"
    ]
    record = {
        "schema": "IMA-LEARNING-CONCLUSION-1.0",
        "conclusion_id": _id(topic + "|" + conclusion),
        "time": time.time(),
        "topic": topic,
        "conclusion": conclusion,
        "evidence_state": evidence_state,
        "evidence": event.get("evidence", []),
        "limitations": event.get("limitations", []),
        "remaining_questions": remaining,
        "next_stages": ["RESEARCH", "TEST", "VERIFY", "TEACH"],
    }
    STATE.mkdir(parents=True, exist_ok=True)
    with FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return record
