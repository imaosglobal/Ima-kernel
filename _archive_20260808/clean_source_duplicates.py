from pathlib import Path
import json

p=Path("learning/sources/registry.json")

data=json.loads(p.read_text(encoding="utf8"))

seen=set()
clean=[]

for s in data["sources"]:
    name=s.get("name")
    if name not in seen:
        clean.append(s)
        seen.add(name)

data["sources"]=clean

p.write_text(
    json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf8"
)

print("REMOVED DUPLICATES")
print("TOTAL SOURCES:",len(clean))
