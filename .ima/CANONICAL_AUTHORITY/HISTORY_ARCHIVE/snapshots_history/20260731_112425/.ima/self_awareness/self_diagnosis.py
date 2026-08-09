import json
from pathlib import Path
from datetime import datetime

KNOWLEDGE=Path(".ima/self_awareness/system_knowledge.json")
AWARENESS=Path(".ima/self_awareness/awareness_state.json")
LESSONS=Path(".ima/self_awareness/long_term_memory.json")


def load(path, default):
    if not path.exists():
        return default

    return json.loads(path.read_text())


def diagnose():

    knowledge=load(KNOWLEDGE,{})
    awareness=load(AWARENESS,{})
    lessons=load(LESSONS,{"lessons":[]})


    result={
        "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "system":{
            "stable":
            knowledge.get("system",{}).get("stable",False),

            "events":
            knowledge.get("system",{}).get("events_total",0)
        },

        "conversation":{
            "active":
            knowledge.get("conversation",{}).get("active",False)
        },

        "learning":{
            "lessons":
            len(lessons.get("lessons",[]))
        },

        "reflection":
        awareness.get("patterns",[])
    }


    return result


def human():

    d=diagnose()

    text=[]

    text.append("=== IMA SELF DIAGNOSIS ===")
    text.append("")

    text.append(
        f"Stable: {d['system']['stable']}"
    )

    text.append(
        f"Events: {d['system']['events']}"
    )

    text.append(
        f"Lessons: {d['learning']['lessons']}"
    )

    text.append("")

    text.append("Reflection:")

    for x in d["reflection"]:
        text.append(
            "- "+x
        )

    return "\n".join(text)


if __name__=="__main__":
    print(human())
