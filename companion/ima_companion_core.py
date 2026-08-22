import json
import time
from pathlib import Path

STATE=Path(".ima/governance/companion_state.json")

def create_companion():
    data={
        "system":"IMA Companion Layer",
        "version":"v1",
        "roles":[
            "child_companion",
            "parent_support",
            "adult_assistant",
            "learning_partner"
        ],
        "principles":[
            "safety_first",
            "privacy_first",
            "human_support",
            "adaptive_learning"
        ],
        "created":time.time()
    }

    STATE.parent.mkdir(parents=True,exist_ok=True)
    STATE.write_text(
        json.dumps(data,ensure_ascii=False,indent=2),
        encoding="utf-8"
    )

    return data


if __name__=="__main__":
    ensure_ascii=False,
    indent=2))
