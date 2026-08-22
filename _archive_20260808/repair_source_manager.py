from pathlib import Path
import py_compile

p = Path("learning/source_manager.py")

p.write_text("""
from learning.source_registry import SourceRegistry
from learning.sources.auto_loader import load_sources
from learning.knowledge_core.source_router import choose_sources
from learning.sources.external_registry import register_external


registry = SourceRegistry()

ACTIVE_SOURCES = load_sources(registry)

register_external(registry)


def collect(question):

    route = choose_sources(question)

    allowed = set(
        route.get("sources", [])
    )

    results = []

    for item in registry.collect(question):

        name = (
            item.get("source")
            or item.get("registry_source")
            or ""
        )

        if not allowed or name in allowed:
            results.append(item)

    return results


def source_status():

    return ACTIVE_SOURCES
""", encoding="utf8")


py_compile.compile(
    str(p),
    doraise=True
)

