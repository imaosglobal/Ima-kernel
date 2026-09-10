"""
Canonical source promotion gate.

Promotion never generates or executes Python code.

A discovered source can only become a pending registry definition.
Runtime activation requires a separate validation/promotion step.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "learning" / "sources" / "registry.json"
CANDIDATES = ROOT / "learning" / "sources" / "candidates.json"


def _module_to_path(module: str) -> Path | None:
    if not isinstance(module, str):
        return None

    prefix = "learning.sources."
    if not module.startswith(prefix):
        return None

    relative = module[len(prefix):]

    if not relative or "/" in relative or "\\" in relative:
        return None

    path = ROOT / "learning" / "sources" / (relative.replace(".", "/") + ".py")

    try:
        path.resolve().relative_to((ROOT / "learning" / "sources").resolve())
    except ValueError:
        return None

    return path


def _existing_handler(module: str, function: str) -> bool:
    path = _module_to_path(module)

    if path is None or not path.is_file():
        return False

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, UnicodeError):
        return False

    return any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == function
        for node in tree.body
    )


def promote() -> list[str]:
    if not REGISTRY.exists() or not CANDIDATES.exists():
        return []

    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(registry, dict):
        return []

    if not isinstance(candidates, list):
        return []

    registry_sources = registry.setdefault("sources", [])

    if not isinstance(registry_sources, list):
        return []

    existing = {
        (
            str(item.get("name", "")).casefold(),
            str(item.get("module", "")).casefold(),
        )
        for item in registry_sources
        if isinstance(item, dict)
    }

    added: list[str] = []

    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue

        if candidate.get("status") != "approved":
            continue

        name = candidate.get("name")
        module = candidate.get("module")
        function = candidate.get("function", "search")

        if not isinstance(name, str) or not name.strip():
            continue

        if not isinstance(module, str) or not isinstance(function, str):
            continue

        # External/legacy registries are not valid promotion targets.
        # A promoted source must have its own canonical source module.
        if module == "learning.sources.external_registry":
            candidate["status"] = "pending_validation"
            candidate["promotion_reason"] = "legacy_external_registry_forbidden"
            continue

        key = (name.casefold(), module.casefold())

        if key in existing:
            continue

        # Critical safety gate:
        # promotion accepts only an already-existing local handler.
        # It never calls source_generator and never imports the module.
        if not _existing_handler(module, function):
            candidate["status"] = "pending_validation"
            candidate["promotion_reason"] = "local_handler_missing_or_invalid"
            continue

        registry_sources.append(
            {
                "name": name,
                "module": module,
                "function": function,
                "priority": 50,
                "enabled": False,
                "trust": "medium",
                "status": "pending_validation",
            }
        )

        existing.add(key)
        candidate["status"] = "pending_validation"
        candidate["promotion_reason"] = "awaiting_runtime_validation"
        added.append(name)

    REGISTRY.write_text(
        json.dumps(
            registry,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    CANDIDATES.write_text(
        json.dumps(
            candidates,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return added
