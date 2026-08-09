from pathlib import Path
import json
from collections import Counter

src=Path(".ima/ima_dependency_map.json")
out=Path(".ima/ima_runtime_map.json")

data=json.loads(src.read_text())

IGNORE=[
    ".ima/archive",
    ".ima/backups",
    "backup",
    "snapshot",
    "__pycache__",
    "node_modules"
]

modules={}

for module,info in data["python_modules"].items():

    if any(x in module for x in IGNORE):
        continue

    modules[module]=info


incoming=Counter()
outgoing=Counter()

for module,info in modules.items():

    outgoing[module]=len(info["imports"])

    for imp in info["imports"]:
        incoming[imp]+=1


report={
    "identity":"IMA",
    "type":"runtime_only",
    "active_python_modules":len(modules),
    "most_imported":incoming.most_common(30),
    "most_active":outgoing.most_common(30)
}


out.write_text(
    json.dumps(
        report,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)


print("=== IMA RUNTIME MAP ===")
print("Active modules:",len(modules))

print("\nMOST CONNECTED:")
for x in incoming.most_common(20):
    print(x)

print("\nMOST ACTIVE:")
for x in outgoing.most_common(20):
    print(x)

print("\nSaved:",out)
