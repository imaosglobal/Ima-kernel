import json
import os
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CHARTER = ROOT / ".ima" / "evolution" / "UNIVERSAL_INTELLIGENCE_CHARTER.json"
GRAPH = ROOT / ".ima" / "evolution" / "CAPABILITY_GRAPH.json"
STATE = ROOT / ".ima" / "evolution" / "STATE.json"

def load(path: Path, default: Any):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

def save(path: Path, value: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def reconcile():
    charter = load(CHARTER, {})
    graph = load(GRAPH, {})
    state = load(STATE, {})
    state.update({
        "schema_version": "1.0",
        "last_run": time.time(),
        "mission": charter.get("mission"),
        "knowledge_scope": charter.get("knowledge_scope"),
        "learning_loop": charter.get("learning_loop"),
        "capability_node_types": graph.get("node_types", []),
        "continuous_benchmarking": charter.get("optimization", {}).get("continuous_benchmarking", True),
        "multi_engine_composition": charter.get("optimization", {}).get("multi_engine_composition", True),
        "truth_rules_active": charter.get("rules", {}),
        "external_manifests_seen": bool(os.getenv("IMA_ENGINE_MANIFEST_JSON", "").strip())
    })
    save(STATE, state)
    return state

if __name__ == "__main__":
    print(json.dumps(reconcile(), ensure_ascii=False, indent=2))
