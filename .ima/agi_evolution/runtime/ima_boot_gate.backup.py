from pathlib import Path
import json,time,subprocess,sys

ROOT=Path(".ima/agi_evolution/runtime")

def load(name):
    p=ROOT/name
    if p.exists():
        return json.loads(p.read_text())
    return {}

def boot():

    state={
        "time":time.time(),
        "boot":"active",
        "source":"ima_boot_gate",
        "runtime":load("ima_master_state.json"),
        "brain":load("brain_state.json"),
        "decision":load("decision_state.json"),
        "handoff":"kernel_ready"
    }

    (ROOT/"boot_gate_state.json").write_text(
        json.dumps(state,indent=2,ensure_ascii=False)
    )

    return state


if __name__=="__main__":
    print(json.dumps(boot(),indent=2,ensure_ascii=False))
