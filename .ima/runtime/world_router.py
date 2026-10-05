"""IMA runtime bridge: World Request -> Capability Graph -> Engine Registry."""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / ".ima" / "engines" / "REGISTRY.json"
GRAPH = ROOT / ".ima" / "evolution" / "CAPABILITY_GRAPH.json"
ROUTABLE = {"connected", "verified", "benchmarked", "routable", "available_via_connected_runtime", "discovered_available"}

def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def load_runtime() -> tuple[dict[str, Any], dict[str, Any]]:
    return _load(REGISTRY), _load(GRAPH)

def route(request: Mapping[str, Any]) -> dict[str, Any]:
    registry, graph = load_runtime()
    intent = str(request.get("intent", ""))
    requested = list(request.get("capabilities", [])) or _infer_capabilities(intent)
    candidates = []
    for engine in registry.get("verified_or_connected_engines", []):
        if engine.get("status") in ROUTABLE and set(requested).issubset(set(engine.get("capabilities", []))):
            candidates.append(engine)
    return {
        "intent": intent,
        "requested_capabilities": requested,
        "candidates": candidates,
        "capability_first": graph.get("routing", {}).get("select_by_capability_first", True),
        "verification_required": registry.get("policy", {}).get("require_verified_capability_before_runtime_use", True),
        "truth_state": "routing_plan_only"
    }

def _infer_capabilities(intent: str) -> list[str]:
    text = intent.lower()
    if any(w in text for w in ("image", "picture", "logo", "visual")): return ["image_generation"]
    if any(w in text for w in ("video", "film", "animation")): return ["video_generation"]
    return []

if __name__ == "__main__":
    payload = json.loads(__import__("sys").stdin.read() or "{}")
    print(json.dumps(route(payload), ensure_ascii=False, indent=2))
