from pathlib import Path
import json

p = Path("learning/sources/registry.json")

data = json.loads(p.read_text(encoding="utf8"))

activate = {
    "PubMed": {
        "module": "learning.sources.pubmed",
        "function": "search"
    },
    "NASA": {
        "module": "learning.sources.nasa",
        "function": "search"
    },
    "Nature": {
        "module": "learning.sources.nature",
        "function": "search"
    },
    "NOAA": {
        "module": "learning.sources.noaa",
        "function": "search"
    }
}

for s in data["sources"]:
    name=s.get("name")

    if name in activate:
        s["enabled"]=True
        s["module"]=activate[name]["module"]
        s["function"]=activate[name]["function"]


p.write_text(
    json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf8"
)

