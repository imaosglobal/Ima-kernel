
from pathlib import Path
import json

LESSONS=Path(".ima/system_learning.jsonl")

def load_context():

    rules=[]
    lessons=[]

    if LESSONS.exists():
        try:
            with LESSONS.open(encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        x=json.loads(line)

                        if x.get("type")=="SYSTEM_RULE":
                            rules.append(x.get("rule"))

                        if x.get("type") in [
                            "SYSTEM_LEARNING",
                            "AUTO_LESSON"
                        ]:
                            lessons.append(x)

        except Exception:
            pass

    return {
        "rules":rules[-20:],
        "lessons":lessons[-20:]
    }
