"""
Compatibility entry point for loading canonical learning sources.

The actual registry implementation lives in learning.source_registry.
This module intentionally contains no independent import/registration logic.
"""

from learning.source_registry import SourceRegistry, load_sources as _load_sources


def load_sources(registry: SourceRegistry):
    """Load validated source definitions into the supplied canonical registry."""
    return _load_sources(registry)
