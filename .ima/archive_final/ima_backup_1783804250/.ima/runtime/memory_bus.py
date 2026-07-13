import json
import time

LOG = ".ima/memory_log.jsonl"

def log_event(event_type, data):
    entry = {
        "ts": time.time(),
        "type": event_type,
        "data": data
    }
    with open(LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
