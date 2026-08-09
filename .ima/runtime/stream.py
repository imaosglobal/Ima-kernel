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

    return event
