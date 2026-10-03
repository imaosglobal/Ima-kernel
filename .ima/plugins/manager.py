"""IMA capability/plugin registry."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(__file__).with_name("REGISTRY.json")

def load_registry() -> dict[str, Any]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

def capabilities() -> dict[str, list[str]]:
    return load_registry().get("routing", {})

def connected_plugins() -> list[dict[str, Any]]:
    return load_registry().get("connected", [])

def route(capability: str) -> list[str]:
    return list(capabilities().get(capability, []))

def is_connected(plugin_id: str) -> bool:
    return any(p.get("id") == plugin_id for p in connected_plugins())
