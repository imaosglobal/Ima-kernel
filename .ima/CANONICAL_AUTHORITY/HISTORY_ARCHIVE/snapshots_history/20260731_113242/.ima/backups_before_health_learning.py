import json
import os
import time
import sys
from pathlib import Path

sys.path.insert(0, ".ima")

ROOT=Path(".")
STATE=Path(".ima/observer/system_state.json")
REGISTRY=Path(".ima/observer/component_registry.json")

def check_component(name,data):

    path=ROOT / data["path"]

    result={
        "name":name,
        "status":"OK" if path.exists() else "MISSING",
        "path":str(path)
    }

    return result


def collect():

    registry=json.load(open(REGISTRY))

    components=[]

    for name,data in registry.items():
        components.append(
            check_component(name,data)
        )


    health=sum(
        1 for x in components
        if x["status"]=="OK"
    )

    score=int(
        health /
        len(components)
        *100
    )


    state={
        "time":time.strftime("%Y-%m-%d %H:%M:%S"),
        "health":score,
        "components":components
    }


    STATE.write_text(
        json.dumps(
            state,
            indent=2,
            ensure_ascii=False
        )
    )

    # ============================================================
    # SELF AWARENESS EVENT: HEALTH CHECK COMPLETED
    # ============================================================
    try:
        from self_awareness.event_bridge import emit

        emit(
            "health_check_completed",
            {
                "health": score,
                "components": len(components)
            }
        )

    except Exception:
        pass


    return state



def guardian(state):

    repairs=[]

    for c in state["components"]:

        if c["status"]!="OK":

            repairs.append(
                {
                "component":c["name"],
                "action":"inspection_required"
                }
            )


    return repairs



if __name__=="__main__":

    state=collect()

    print("=== IMA SYSTEM STATUS ===")

    for c in state["components"]:
        print(
            c["name"],
            "🟢" if c["status"]=="OK" else "🔴",
            c["status"]
        )

    print()
    print(
        "HEALTH:",
        state["health"],
        "%"
    )

    print()
    print(
        "GUARDIAN:",
        guardian(state)
    )
