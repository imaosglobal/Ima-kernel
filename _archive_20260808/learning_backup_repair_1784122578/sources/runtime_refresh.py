from learning.source_manager import registry
from learning.sources.auto_loader import load_sources


def refresh_sources():

    registry.sources.clear()

    load_sources(registry)

    return [
        s["name"]
        for s in registry.sources
    ]
