from pathlib import Path
import json,time

ROOT=Path(".ima/agi_evolution/runtime")

def decide():

    master=json.loads(
        (ROOT/"ima_master_state.json").read_text()
    )

    decision={
        "time":time.time(),
        "current":master.get("decision"),
        "next_action":"continue_evolution_cycle",
        "priority":"stability"
    }

    (ROOT/"decision_state.json").write_text(
        json.dumps(decision,indent=2,ensure_ascii=False)
    )

    return decision


if __name__=="__main__":
    print(json.dumps(decide(),indent=2))
