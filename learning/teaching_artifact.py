"""Create provenance-preserving teaching records from verified knowledge."""

from __future__ import annotations
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".ima" / "teaching"
FILE = STATE / "artifacts.jsonl"

def _id(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]

def create_teaching_artifact(event: Dict[str, Any]) -> Dict[str, Any]:
    topic = str(event.get("topic") or "general").strip()
    artifact = {
        "schema": "IMA-TEACHING-ARTIFACT-1.0",
        "artifact_id": _id(topic + "|" + str(event.get("content", ""))),
        "time": time.time(),
        "topic": topic,
        "evidence_state": event.get("evidence_state", "UNVERIFIED"),
        "content": event.get("content", ""),
        "audience": event.get("audience", ["general"]),
        "languages": event.get("languages", ["source"]),
        "prerequisites": event.get("prerequisites", []),
        "examples": event.get("examples", []),
        "provenance": event.get("provenance", []),
        "limitations": event.get("limitations", []),
    }
    STATE.mkdir(parents=True, exist_ok=True)
    with FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(artifact, ensure_ascii=False, sort_keys=True) + "\n")
    return artifact
