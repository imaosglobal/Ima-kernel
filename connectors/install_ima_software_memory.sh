#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/ima_kernel/connectors"

mkdir -p \
"$BASE/intelligence" \
"$BASE/scanner" \
"$BASE/knowledge" \
"$HOME/.ima"

cat > "$BASE/knowledge/software_memory.jsonl" <<'EOF'
EOF

cat > "$BASE/knowledge/patterns.json" <<'EOF'
{
 "patterns":[]
}
EOF

cat > "$BASE/knowledge/capability_graph.json" <<'EOF'
{
 "nodes":{},
 "relations":{}
}
EOF


cat > "$BASE/intelligence/knowledge_engine.py" <<'PY'
import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent
MEMORY = BASE / "knowledge/software_memory.jsonl"
GRAPH = BASE / "knowledge/capability_graph.json"

def now():
    return datetime.now().isoformat()


def load():
    data={}
    if MEMORY.exists():
        for line in MEMORY.read_text().splitlines():
            try:
                item=json.loads(line)
                key=item["concept"]+"::"+item["source"]
                data[key]=item
            except:
                pass
    return data


def save(data):
    with open(MEMORY,"w",encoding="utf-8") as f:
        for item in data.values():
            f.write(json.dumps(item,ensure_ascii=False)+"\n")


def learn(concept,source,confidence=0.5):
    data=load()
    key=concept+"::"+source

    if key in data:
        data[key]["confidence"]=max(
            data[key]["confidence"],
            confidence
        )
        data[key]["last_updated"]=now()
    else:
        data[key]={
            "concept":concept,
            "source":source,
            "confidence":confidence,
            "first_seen":now(),
            "last_updated":now()
        }

    save(data)


def update_graph():
    data=load()

    graph={
        "nodes":{},
        "relations":{}
    }

    for item in data.values():
        graph["nodes"].setdefault(
            item["concept"],[]
        ).append(item["source"])

    for concept,sources in graph["nodes"].items():
        if len(sources)>1:
            graph["relations"][
                concept
            ]="shared_capability"

    GRAPH.write_text(
        json.dumps(
            graph,
            indent=2,
            ensure_ascii=False
        )
    )


if __name__=="__main__":
    learn("inventory","erp",0.9)
    learn("customers","crm",0.9)
    learn("payments","pos",0.8)
    update_graph()
PY


cat > "$BASE/scanner/scanner_agent.py" <<'PY'
import json
from pathlib import Path
import sys

sys.path.append(
    str(Path(__file__).parent.parent / "intelligence")
)

from knowledge_engine import learn,update_graph


SOURCES=[
 {
  "name":"beecomm",
  "type":"pos",
  "abilities":[
   "sales",
   "inventory",
   "customers"
  ]
 },
 {
  "name":"odoo",
  "type":"erp",
  "abilities":[
   "accounting",
   "inventory",
   "business_processes"
  ]
 },
 {
  "name":"shopify",
  "type":"ecommerce",
  "abilities":[
   "products",
   "orders",
   "customers"
  ]
 }
]


for software in SOURCES:
    for ability in software["abilities"]:
        learn(
            ability,
            software["name"],
            0.8
        )

update_graph()

 "SCAN COMPLETE:",
 len(SOURCES),
 "software profiles"
)
PY


cat > "$BASE/intelligence/ima_knowledge_api.py" <<'PY'
import json
from pathlib import Path

MEMORY=Path(__file__).parent.parent / "knowledge/software_memory.jsonl"


def query():
    result=[]

    if MEMORY.exists():
        for line in MEMORY.read_text().splitlines():
            result.append(json.loads(line))

    return result


if __name__=="__main__":
        json.dumps(
            query(),
            indent=2,
            ensure_ascii=False
        )
    )
PY


cat > "$HOME/.ima/software_memory_bridge.sh" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
python $BASE/scanner/scanner_agent.py
python $BASE/intelligence/knowledge_engine.py
EOF

chmod +x "$HOME/.ima/software_memory_bridge.sh"

echo "IMA SOFTWARE MEMORY INSTALLED"
