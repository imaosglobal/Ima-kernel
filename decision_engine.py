import json
from pathlib import Path


p=Path.home()/".ima/evolution/evolution_brain.json"
p.parent.mkdir(parents=True, exist_ok=True)

data=json.loads(p.read_text())


actions=data.get(
    "next_actions",
    []
)


for a in actions:

    if a["priority"]==1:
        a["decision"]="DO_FIRST"


data["decisions"]=actions


p.write_text(
    json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )
)


