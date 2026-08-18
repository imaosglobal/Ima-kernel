from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib

ROOT = Path(".")
CANON = ROOT / ".ima/CANONICAL_AUTHORITY/SINGLE_SNAPSHOT/CURRENT"
CONT = CANON / ".ima/continuity"

STATE = CONT / "generation_state.json"
MANIFEST = CONT / "CONTINUITY_MANIFEST.json"
RUNTIME_BRIDGE = CONT / "runtime_bridge.json"

STREAM = ROOT / ".ima/continuity_stream.jsonl"

def _load(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def _utc():
    return datetime.now(timezone.utc).isoformat()

def _generation():
    state = _load(STATE, {})
    return int(state.get("generation", 1))

def record_event(event_type, data=None):
    """
    Canonical continuity boundary.

    Every runtime event receives:
      - generation
      - timestamp
      - event type
      - payload
      - previous hash
      - current hash

    The continuity stream is append-only.
    """
    data = data or {}

    previous_hash = ""
    if STREAM.exists():
        try:
            last = STREAM.read_text(encoding="utf-8").splitlines()[-1]
            previous_hash = json.loads(last).get("hash", "")
        except Exception:
            pass

    event = {
        "type": event_type,
        "ts": _utc(),
        "generation": _generation(),
        "continuity": True,
        "payload": data,
        "previous_hash": previous_hash,
    }

    canonical = json.dumps(
        event,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":")
    )

    event["hash"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    STREAM.parent.mkdir(parents=True, exist_ok=True)
    with STREAM.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    return event

def continuity_status():
    return {
        "active": True,
        "generation": _generation(),
        "stream": str(STREAM),
        "canonical_root": str(CANON),
    }
