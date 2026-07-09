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
    except:
        return []

def load_state_machine():
    try:
        with open(STATE_MACHINE) as f:
            return json.load(f)
    except:
        return {"states": {}}


def build_core():
    events = load_events()
    core = reduce(events)
    core["state"] = "INIT"

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
