import json
import time
import sys
from pathlib import Path

# ------------------------------------------------------------
# IMA CANONICAL EVENT BUS
# Single event boundary:
#
#   connector
#       -> emit()
#       -> normalize
#       -> dedupe
#       -> continuity
#       -> ima.stream.jsonl
#       -> memory_log.jsonl
# ------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

MEMORY_LOG = ROOT / ".ima" / "memory_log.jsonl"
STREAM_LOG = ROOT / ".ima" / "ima.stream.jsonl"

RUNTIME_DIR = Path(__file__).resolve().parent
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))


# ------------------------------------------------------------
# Continuity
# ------------------------------------------------------------

try:
    from continuity_runtime import record_event
except Exception:
    record_event = None


# ------------------------------------------------------------
# Canonical event names
# ------------------------------------------------------------

EVENT_ALIASES = {
    "whatsapp.message.received": "whatsapp.message_received",
    "whatsapp.message_received": "whatsapp.message_received",

    "whatsapp.message.sent": "whatsapp.message_sent",
    "whatsapp.message_sent": "whatsapp.message_sent",
}


def normalize_event_type(event_type: str) -> str:
    return EVENT_ALIASES.get(event_type, event_type)


# ------------------------------------------------------------
# Persistence
# ------------------------------------------------------------

def _append(path: Path, event: dict):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(event, ensure_ascii=False) + "\n"
        )


# ------------------------------------------------------------
# Monitor
# ------------------------------------------------------------

def update_monitor():
    try:
        import ima_live_monitor
        ima_live_monitor.build_status()
    except Exception:
        pass


# ------------------------------------------------------------
# Canonical emit()
# ------------------------------------------------------------

def emit(event_type, **data):
    """
    THE canonical IMA event boundary.

    Every event passes through here.

    WhatsApp legacy names are normalized here.
    Persistent WhatsApp deduplication happens here.
    Events are persisted to both:
        .ima/ima.stream.jsonl
        .ima/memory_log.jsonl
    """

    # 1. Normalize FIRST
    event_type = normalize_event_type(event_type)

    # 2. Persistent deduplication for incoming WhatsApp messages
    if event_type == "whatsapp.message_received":

        user_id = data.get("user_id")
        message = data.get("message")

        if user_id is not None and message is not None:

            try:
                from message_dedupe import accept as _ima_accept
            except Exception:
                _ima_accept = None

            if _ima_accept is not None:
                if not _ima_accept(user_id, message):
                    return None

    # 3. Create ONE canonical event object
    event = {
        "type": event_type,
        "ts": time.time(),
        **data,
    }

    # 4. Continuity hook
    if record_event is not None:
        try:
            record_event(event_type, data)
        except Exception:
            pass

    # 5. Canonical event stream
    _append(STREAM_LOG, event)

    # 6. Canonical memory log
    memory_event = {
        "type": event_type,
        "source": "stream",
        **data,
    }

    _append(MEMORY_LOG, memory_event)

    # 7. Update live system status
    update_monitor()

    return event
