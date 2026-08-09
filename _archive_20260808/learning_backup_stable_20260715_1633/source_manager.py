from learning.source_registry import SourceRegistry
from learning.sources.auto_loader import load_sources


registry = SourceRegistry()

ACTIVE_SOURCES = load_sources(
    registry
)


def collect(question):

    return registry.collect(
        question
    )


def source_status():

    return ACTIVE_SOURCES
