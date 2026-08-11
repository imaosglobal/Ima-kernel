import json
import time
import os
from pathlib import Path

MEMORY_LOG = Path(".ima/memory_log.jsonl")
STREAM = ".ima/ima.stream.jsonl"


def update_monitor():
    try:
        import ima_live_monitor
        ima_live_monitor.build_status()
    except Exception as e:
        pass


def emit(event_type, **data):

    event = {
        "type": event_type,
        "ts": time.time(),
        **data
    }

    os.makedirs(os.path.dirname(STREAM), exist_ok=True)

    with open(STREAM, "a") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


    with open(MEMORY_LOG, "a") as f:
        f.write(json.dumps({
            "type": event_type,
            "source": "stream",
            **data
        }, ensure_ascii=False) + "\n")


    update_monitor()

    # Optional real-time IMA -> WhatsApp reporting.
    # Disabled unless WA_REPORT_TO is explicitly configured.
    if os.getenv("WA_REPORT_TO") and not event_type.startswith("whatsapp."):
        try:
            from pathlib import Path as _Path
            import sys as _sys

            _wa_dir = _Path(".ima/CANONICAL_AUTHORITY/SINGLE_SNAPSHOT/CURRENT/connectors/whatsapp")
            if str(_wa_dir) not in _sys.path:
                _sys.path.insert(0, str(_wa_dir))

            from whatsapp_connector import WhatsAppConnector

            report = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
            WhatsAppConnector().send_message(
                os.getenv("WA_REPORT_TO"),
                "IMA LIVE EVENT\n" + report
            )
        except Exception as _e:
            # Reporting must never break IMA's event bus.
            try:
                with open(".ima/whatsapp.log", "a", encoding="utf-8") as _f:
                    _f.write("LIVE_REPORT_ERROR: " + str(_e) + "\\n")
            except Exception:
                pass

    return event
