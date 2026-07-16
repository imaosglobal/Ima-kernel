from pathlib import Path
import json,time

ROOT=Path(".ima/agi_evolution/runtime")

files=[
"evolution_history.json",
"brain_state.json",
"supervisor_state.json",
"decision_state.json"
]

memory={
"time":time.time(),
"sources":{}
}

for f in files:
    p=ROOT/f
    if p.exists():
        memory["sources"][f]=json.loads(p.read_text())

(ROOT/"ima_long_term_memory.json").write_text(
json.dumps(memory,indent=2,ensure_ascii=False)
)

print("memory consolidated")
