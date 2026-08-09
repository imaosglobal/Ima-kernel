import json
import time
import os

STREAM = ".ima/ima.stream.jsonl"

def emit(event_type, **data):
    event = {
        "type": event_type,
        "ts": time.time(),
        **data
    }
    os.makedirs(os.path.dirname(STREAM), exist_ok=True)
    with open(STREAM, "a") as f:
        f.write(json.dumps(event) + "\n")
