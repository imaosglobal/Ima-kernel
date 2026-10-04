"""Canonical runtime capability router.

This module connects IMA's registry, capability-gap queue, and truth policy into
one read-only runtime view. It never authenticates or installs third-party
providers and never promotes a capability without executable evidence.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / ".ima" / "plugins" / "REGISTRY.json"
GAP_QUEUE_PATH = ROOT / ".ima" / "plugins" / "gap_queue.py"
FABRIC_PATH = ROOT / ".ima" / "integration" / "UNIVERSAL_INTEGRATION_FABRIC.md"
INFLUENCE_POLICY_PATH = ROOT / ".ima" / "integration" / "INFLUENCE_POLICY.json"


def _load_gap_queue():
    spec = importlib.util.spec_from_file_location("ima_gap_queue_runtime", GAP_QUEUE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("gap queue module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.CapabilityGapQueue()


def load_registry() -> Dict[str, Any]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def connected_providers(registry: Optional[Dict[str, Any]] = None) -> list[Dict[str, Any]]:
    data = registry or load_registry()
    return [
        item for item in data.get("connected", [])
        if item.get("status", "connected") in {"connected", "ready", "implemented_not_yet_production_verified"}
    ]


def provider_candidates(capability: str, registry: Optional[Dict[str, Any]] = None) -> list[Dict[str, Any]]:
    matches = []
    for item in connected_providers(registry):
        if capability in item.get("capabilities", []):
            matches.append({
                "id": item.get("id"),
                "provider": item.get("provider"),
                "status": item.get("status", "connected"),
            })
    return matches


def capability_status(capability: str, registry: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = registry or load_registry()
    candidates = provider_candidates(capability, data)
    verified = [
        item for item in candidates
        if item.get("status") == "connected"
    ]
    return {
        "capability": capability,
        "available": bool(verified),
        "candidates": candidates,
        "verified_provider_count": len(verified),
        "claim_policy": data.get("policy", {}).get("require_verified_capability_before_claiming", True),
    }


def snapshot() -> Dict[str, Any]:
    registry = load_registry()
    queue = _load_gap_queue()
    return {
        "schema": "IMA-CAPABILITY-RUNTIME-1.1",
        "universal_integration_fabric": {
            "present": FABRIC_PATH.exists(),
            "policy": "discover-describe-map-authorize-connect-execute-observe-verify-learn-generalize-document-monitor-reassess",
        },
        "learning_governance": {
            "present": INFLUENCE_POLICY_PATH.exists(),
            "bounded_verified_learning_only": True,
        },
        "providers": connected_providers(registry),
        "routes": registry.get("routing", {}),
        "next_gap": queue.next_gap(),
        "gap_snapshot": queue.snapshot(),
        "policy": registry.get("policy", {}),
    }


def route(capability: str) -> Dict[str, Any]:
    status = capability_status(capability)
    if status["available"]:
        status["route"] = status["candidates"][0]
        status["truth_state"] = "connected"
        status["execution_allowed"] = True
    else:
        status["route"] = None
        status["truth_state"] = "discovered_or_missing"
        status["execution_allowed"] = False
    return status
