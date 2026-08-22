import json
import sys
sys.path.insert(0, '.ima')
from ima_reducer import reduce

LEDGER = ".ima/ledger.jsonl"
STATE_MACHINE = ".ima/state_machine.json"


def load_events():
    try:
        with open(LEDGER) as f:
            return [json.loads(l) for l in f if l.strip()]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def load_state_machine():
    try:
        with open(STATE_MACHINE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"states": {}}


def can_transition(old, new, sm):
    states = sm.get("states", {})
    allowed = states.get(old, {}).get("next", [])
    return new in allowed


def resolve_state(core, sm):
    states = sm.get("states", {})

    files = core.get("files", [])

    if not files:
        return "INIT"

    current = "INIT"

    if len(files) >= 2:
        current = "INDEXED"

    if "graph" in core:
        current = "AWARE"

    return current


def load_previous_state():
    try:
        with open(".ima/core_map.json") as f:
            return json.load(f).get("state", "INIT")
    except (FileNotFoundError, json.JSONDecodeError):
        return "INIT"


def emit_state_change(old, new):
    if old == new:
        return

    import time

    event = {
        "ts": time.time(),
        "type": "STATE_CHANGE",
        "data": {
            "from": old,
            "to": new
        }
    }

    with open(LEDGER, "a") as f:
        f.write(json.dumps(event) + "\\n")


def emit_state_change(old, new):
    if old == new:
        return

    import time

    event = {
        "ts": time.time(),
        "type": "STATE_CHANGE",
        "data": {
            "from": old,
            "to": new
        }
    }

    with open(LEDGER, "a") as f:
        f.write(json.dumps(event) + "\\n")


def build_core():
    events = load_events()
    core = reduce(events)

    sm = load_state_machine()
    old_state = load_previous_state()
    new_state = resolve_state(core, sm)

    if can_transition(old_state, new_state, sm):
        core["state"] = new_state
        emit_state_change(old_state, new_state)
    else:
        core["state"] = old_state

    with open(".ima/core_map.json", "w") as f:
        json.dump(core, f, indent=2)

    return core

def status():
    core = build_core()

    print("=== IMA EVENT KERNEL ===")
    print("FILES:", len(core.get("files", [])))
    print("MODE:", core.get("mode"))

if __name__ == "__main__":
    status()
