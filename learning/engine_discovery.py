import json
import os
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / ".ima" / "engines" / "REGISTRY.json"
STATE_PATH = ROOT / ".ima" / "engines" / "DISCOVERY_STATE.json"

DISCOVERY_HINTS = {
    "openai": "https://developers.openai.com/api/docs/changelog",
    "runway": "https://docs.dev.runwayml.com/",
    "openart": "https://openart.ai/"
}

def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def discover_from_environment() -> list[dict[str, Any]]:
    raw = os.getenv("IMA_ENGINE_MANIFEST_JSON", "").strip()
    if not raw:
        return []
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError("IMA_ENGINE_MANIFEST_JSON must be a JSON list")
    return [x for x in data if isinstance(x, dict)]

def normalize(candidate: dict[str, Any]) -> dict[str, Any]:
    required = ("id", "provider", "family", "capabilities")
    missing = [k for k in required if not candidate.get(k)]
    if missing:
        raise ValueError("engine candidate missing: " + ",".join(missing))
    return {
        "id": str(candidate["id"]),
        "provider": str(candidate["provider"]),
        "family": str(candidate["family"]),
        "capabilities": sorted({str(x) for x in candidate["capabilities"]}),
        "status": candidate.get("status", "discovered"),
        "discovered_at": candidate.get("discovered_at", time.time()),
        "source": candidate.get("source"),
        "selection_role": candidate.get("selection_role", "candidate")
    }

def reconcile(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    registry = load_json(REGISTRY_PATH, {})
    engines = registry.setdefault("verified_or_connected_engines", [])
    by_id = {x.get("id"): x for x in engines if isinstance(x, dict)}
    staged = []
    for raw in candidates:
        item = normalize(raw)
        existing = by_id.get(item["id"])
        if existing:
            existing.update({
                "capabilities": item["capabilities"],
                "source": item.get("source"),
                "last_seen": time.time()
            })
        else:
            item["status"] = "staged"
            engines.append(item)
            by_id[item["id"]] = item
            staged.append(item["id"])
    state = load_json(STATE_PATH, {})
    state.update({
        "last_run": time.time(),
        "discovered_count": len(candidates),
        "staged_ids": staged,
        "routable_ids": [
            x["id"] for x in engines
            if x.get("status") in {
                "connected", "verified", "benchmarked", "routable",
                "available_via_connected_runtime", "discovered_available"
            }
        ],
        "provider_hints": DISCOVERY_HINTS
    })
    save_json(REGISTRY_PATH, registry)
    save_json(STATE_PATH, state)
    return state

def choose_engine(capability: str, user_context: dict[str, Any] | None = None, preferred: list[str] | None = None):
    user_context = user_context or {}
    registry = load_json(REGISTRY_PATH, {})
    engines = registry.get("verified_or_connected_engines", [])
    routable = [
        x for x in engines
        if capability in x.get("capabilities", [])
        and x.get("status") in {
            "connected", "verified", "benchmarked", "routable",
            "available_via_connected_runtime", "discovered_available"
        }
    ]
    order = {name: i for i, name in enumerate(preferred or [])}
    routable.sort(key=lambda x: (
        order.get(x.get("id"), 10000),
        0 if x.get("provider") in user_context.get("preferred_providers", []) else 1,
        x.get("selection_role", "candidate")
    ))
    return routable[0] if routable else None

def main() -> int:
    state = reconcile(discover_from_environment())
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
