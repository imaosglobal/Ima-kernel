import json
from pathlib import Path

BASE=Path(".ima/agi_evolution/world_model")

def add_entity(name,kind):
    f=BASE/"entity_registry.json"
    data=json.loads(f.read_text()) if f.exists() else {"entities":[]}
    data["entities"].append({
        "name":name,
        "type":kind
    })
    f.write_text(json.dumps(data,indent=2,ensure_ascii=False))

def status():
    return {
        "entities":
        len(json.loads((BASE/"entity_registry.json").read_text())["entities"])
        if (BASE/"entity_registry.json").exists()
        else 0
    }
