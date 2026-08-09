import json
from pathlib import Path

KNOWLEDGE=Path(".ima/self_awareness/system_knowledge.json")


def get_knowledge():

    if not KNOWLEDGE.exists():
        return {}

    return json.loads(
        KNOWLEDGE.read_text()
    )


def answer():

    k=get_knowledge()

    return {
        "health":k.get("system",{}).get("stable"),
        "events":k.get("system",{}).get("events_total"),
        "conversation":k.get("conversation",{}).get("active"),
        "lessons":k.get("learning",{}).get("lessons_count")
    }


if __name__=="__main__":
    print(
        json.dumps(
            answer(),
            indent=2,
            ensure_ascii=False
        )
    )
