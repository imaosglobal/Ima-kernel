import json
from pathlib import Path
import time

LOG = Path(".ima/memory_log.jsonl")

def log(event_type, payload):
    event = {
        "type": event_type,
        "ts": time.time(),
        "data": payload
    }

    with open(LOG, "a") as f:
        f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    log("test", {"msg": "hello"})
