import json, time

LEDGER = ".ima/ledger.jsonl"

def emit(event_type, **data):
    event = {
        "ts": time.time(),
        "type": event_type,
        "data": data
    }
    with open(LEDGER, "a") as f:
        f.write(json.dumps(event) + "\n")
