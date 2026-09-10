"""
Canonical IMA source registry.

Single runtime registry for learning/source collection.
Source definitions live in learning/sources/registry.json.

Security rule:
- Registry metadata does NOT imply trust.
- A source must pass structural validation before loading.
- Collection failures are isolated per source.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
REGISTRY_FILE = ROOT / "learning" / "sources" / "registry.json"


class SourceRegistry:
    def __init__(self) -> None:
        self.sources: list[dict[str, Any]] = []

    def register(
        self,
        name: str,
        handler: Callable[[str], Any],
        priority: int = 50,
    ) -> None:
        if not name or not callable(handler):
            return

        normalized_name = str(name).strip().casefold()
        new_priority = int(priority)

        # One canonical runtime entry per source name.
        for index, existing in enumerate(self.sources):
            existing_name = str(existing.get("name", "")).strip().casefold()

            if existing_name != normalized_name:
                continue

            existing_priority = int(existing.get("priority", 0))

            if new_priority > existing_priority:
                self.sources[index] = {
                    "name": name,
                    "handler": handler,
                    "priority": new_priority,
                }

            self.sources.sort(
                key=lambda item: item.get("priority", 0),
                reverse=True,
            )
            return

        self.sources.append(
            {
                "name": name,
                "handler": handler,
                "priority": new_priority,
            }
        )

        self.sources.sort(
            key=lambda item: item.get("priority", 0),
            reverse=True,
        )

    def collect(self, question: str) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []

        for source in list(self.sources):
            handler = source.get("handler")

            if not callable(handler):
                continue

            try:
                result = handler(question)
            except Exception:
                continue

            if result is None:
                continue

            if isinstance(result, dict):
                item = dict(result)
            else:
                item = {
                    "content": str(result),
                }

            item.setdefault("source", source["name"])
            item.setdefault("registry_source", source["name"])
            item.setdefault("priority", source.get("priority", 0))

            results.append(item)

        return results


def _validate_definition(source: dict[str, Any]) -> bool:
    if not isinstance(source, dict):
        return False

    if source.get("enabled") is not True:
        return False

    name = source.get("name")
    module = source.get("module")
    function = source.get("function")

    if not isinstance(name, str) or not name.strip():
        return False

    # Runtime source modules must live inside the canonical source package.
    if not isinstance(module, str) or not module.startswith("learning.sources."):
        return False

    if not isinstance(function, str) or not function.isidentifier():
        return False

    trust = source.get("trust")
    if trust not in {"high", "medium"}:
        return False

    try:
        priority = int(source.get("priority", 0))
    except (TypeError, ValueError):
        return False

    if priority < 0 or priority > 100:
        return False

    return True


def _load_definitions() -> list[dict[str, Any]]:
    if not REGISTRY_FILE.exists():
        return []

    try:
        data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

    sources = data.get("sources", [])
    if not isinstance(sources, list):
        return []

    valid = []

    for source in sources:
        if _validate_definition(source):
            valid.append(source)

    return valid


def load_sources(registry: SourceRegistry) -> list[str]:
    loaded: list[str] = []

    for source in _load_definitions():
        try:
            module = importlib.import_module(source["module"])
            handler = getattr(module, source["function"])

            if not callable(handler):
                continue

            registry.register(
                source["name"],
                handler,
                source.get("priority", 50),
            )
            loaded.append(source["name"])

        except Exception:
            continue

    return loaded


def get_sources() -> list[dict[str, Any]]:
    return _load_definitions()
