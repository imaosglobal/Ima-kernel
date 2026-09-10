# Canonical compatibility adapter.
# All operational memory persistence goes through the canonical executive memory store.

from founder.executive_ai.memory.memory_store import save_memory as _canonical_save_memory


def save_memory(memory):
    if isinstance(memory, dict):
        if not memory:
            return None
        results = []
        for key, value in memory.items():
            results.append(
                _canonical_save_memory(
                    key=str(key),
                    value=value,
                    category="legacy_memory",
                    importance=50,
                )
            )
        return results
    return _canonical_save_memory(
        key="legacy_memory",
        value=memory,
        category="legacy_memory",
        importance=50,
    )
