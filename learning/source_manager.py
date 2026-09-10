from learning.source_registry import SourceRegistry, load_sources
from learning.knowledge_core.source_router import choose_sources
from learning.knowledge_core.source_cleaner import clean_source


# Canonical runtime registry.
registry = SourceRegistry()

# Load only definitions accepted by the canonical registry.
ACTIVE_SOURCES = load_sources(registry)



def collect(question):
    route = choose_sources(question)
    allowed = set(route.get("sources", []))

    results = []

    for item in registry.collect(question):
        name = (
            item.get("source")
            or item.get("registry_source")
            or ""
        )

        if not allowed or name in allowed:
            clean = clean_source(item)
            if clean:
                results.append(clean)

    return results


def source_status():
    return [
        {
            "name": item.get("name"),
            "priority": item.get("priority", 0),
        }
        for item in registry.sources
    ]
