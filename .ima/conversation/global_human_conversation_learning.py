
"""Canonical human-conversation learning layer; child of the single IMA unified loop."""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / ".ima/conversation/inbox.jsonl"
LEDGER = ROOT / ".ima/conversation/learning_ledger.jsonl"
SHARED = ROOT / ".ima/conversation/teaching_queue.jsonl"
VALID = {"ESTABLISHED_FACT","SUPPORTED_FINDING","OPEN_HYPOTHESIS","INTERPRETATION","METAPHOR","UNKNOWN"}
PRIVATE = {"PRIVATE","SENSITIVE","CREDENTIAL","UNAUTHORIZED_SHARE"}

def _record(obj, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def assess(item):
    evidence = item.get("evidence") or []
    counter = item.get("counterevidence") or []
    state = item.get("truth_state", "UNKNOWN")
    if state not in VALID:
        state = "UNKNOWN"
    privacy = item.get("privacy_class", "PRIVATE_UNLESS_EXPLICITLY_SHAREABLE")
    shareable = privacy not in PRIVATE and item.get("consent_scope") in {"PUBLIC","SHAREABLE","EXPLICIT_TEACHING"}
    if counter and state in {"ESTABLISHED_FACT","SUPPORTED_FINDING"}:
        state = "OPEN_HYPOTHESIS"
    if not evidence and state in {"ESTABLISHED_FACT","SUPPORTED_FINDING"}:
        state = "UNKNOWN"
    return {"truth_state": state, "shareable": shareable,
            "needs_verification": state in {"UNKNOWN","OPEN_HYPOTHESIS","INTERPRETATION"}}

def process_once():
    if not QUEUE.exists():
        return {"processed": 0, "promoted": 0, "shared": 0, "status": "READY_EMPTY"}
    lines = [x for x in QUEUE.read_text(encoding="utf-8").splitlines() if x.strip()]
    promoted = shared = 0
    for line in lines:
        item = json.loads(line)
        result = assess(item)
        out = {**item, **result, "processed_at": datetime.now(timezone.utc).isoformat(),
               "processor": "ima.global_human_conversation_learning"}
        _record(out, LEDGER)
        if result["shareable"] and result["truth_state"] in {"ESTABLISHED_FACT","SUPPORTED_FINDING"}:
            _record(out, SHARED); shared += 1
        if result["truth_state"] in {"ESTABLISHED_FACT","SUPPORTED_FINDING"}:
            promoted += 1
    QUEUE.write_text("", encoding="utf-8")
    return {"processed": len(lines), "promoted": promoted, "shared": shared, "status": "PROCESSED"}

if __name__ == "__main__":
    print(json.dumps(process_once(), ensure_ascii=False))
