from pathlib import Path
import json
from datetime import datetime

AUTHORITY = Path(".ima/CANONICAL_AUTHORITY/ACTIVE")

def authority_status():
    return {
        "authority": str(AUTHORITY),
        "exists": AUTHORITY.exists(),
        "timestamp": datetime.now().isoformat()
    }


def emit_learning_event(event, payload=None):
    record = {
        "event": event,
        "payload": payload or {},
        "source": "learning/runtime_bridge",
        "time": datetime.now().isoformat()
    }

    log = Path("learning/runtime_events.jsonl")
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record
