from pathlib import Path
import json
from collections import Counter

src=Path(".ima/ima_dependency_map.json")
out=Path(".ima/ima_control_flow.json")

data=json.loads(src.read_text())

outgoing=Counter()

for module,info in data["python_modules"].items():

    for imp in info["imports"]:
        if not imp.startswith(("json","pathlib","os","sys","datetime","time")):
            outgoing[module]+=1


top=outgoing.most_common(50)

report={
    "identity":"IMA",
    "type":"control_flow_analysis",
    "most_active_modules":top
}


out.write_text(
    json.dumps(
        report,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)



for item in top[:30]:

