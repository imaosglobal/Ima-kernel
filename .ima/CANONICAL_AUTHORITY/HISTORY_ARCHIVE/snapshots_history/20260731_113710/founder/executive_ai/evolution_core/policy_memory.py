from pathlib import Path
import json

FILE = Path("founder/data/policy_memory.json")

def save_rule(rule):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    data.append(rule)

    FILE.parent.mkdir(parents=True, exist_ok=True)
    FILE.write_text(
        json.dumps(data,ensure_ascii=False,indent=2)
    )

    return rule
