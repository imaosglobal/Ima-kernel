from pathlib import Path
import json
from collections import Counter

src=Path(".ima/ima_dependency_map.json")
out=Path(".ima/ima_architecture_report.json")

data=json.loads(src.read_text())

incoming=Counter()

for module,info in data["python_modules"].items():

    for imp in info["imports"]:
        incoming[imp]+=1


top=incoming.most_common(50)


report={
    "identity":"IMA",
    "status":"architecture_analysis",
    "python_modules":data["count"],
    "most_connected_modules":top,
    "possible_core_candidates":[
        x[0] for x in top[:20]
    ]
}


out.write_text(
    json.dumps(
        report,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)



for item in top[:20]:
    
