
from pathlib import Path
import json

LESSONS=Path(".ima/system_learning.jsonl")

def load_lessons():
    result=[]

    if not LESSONS.exists():
        return result

    with LESSONS.open(encoding="utf-8") as f:
        for line in f:
            try:
                if line.strip():
                    result.append(json.loads(line))
            except Exception:
                pass

    return result


def get_rules():
    rules=[]

    for lesson in load_lessons():

        if lesson.get("type")=="SYSTEM_RULE":
            rules.append(
                lesson.get("rule")
            )

        if lesson.get("type")=="SYSTEM_LEARNING":
            details=lesson.get("details",{})
            if "rule" in details:
                rules.append(details["rule"])

    return rules


def context():
    return {
        "lessons_count":len(load_lessons()),
        "rules":get_rules()
    }


if __name__=="__main__":
    print(json.dumps(
        context(),
        ensure_ascii=False,
        indent=2
    ))
