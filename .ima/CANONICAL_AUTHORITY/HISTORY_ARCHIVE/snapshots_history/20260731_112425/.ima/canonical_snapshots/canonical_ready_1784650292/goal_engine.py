import json
from pathlib import Path


p=Path.home()/".ima/evolution/evolution_brain.json"
p.parent.mkdir(parents=True, exist_ok=True)

data=json.loads(p.read_text())


goals=[]


for x in data.get("missing_capabilities",[]):

    goals.append(
        {
        "goal":"create_"+x+"_engine",
        "importance":"high"
        }
    )


data["goals"]=goals


p.write_text(
    json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )
)


print("GOALS GENERATED")
