import json
from pathlib import Path

STATE=Path(".ima/self_awareness/awareness_state.json")


def check():

    if not STATE.exists():
        return {
            "status":"unknown"
        }

    data=json.loads(
        STATE.read_text()
    )

    warnings=[]

    if data.get("total_events",0)==0:
        warnings.append(
            "no_events"
        )

    return {
        "status":"ok" if not warnings else "warning",
        "warnings":warnings
    }


if __name__=="__main__":
    print(check())
