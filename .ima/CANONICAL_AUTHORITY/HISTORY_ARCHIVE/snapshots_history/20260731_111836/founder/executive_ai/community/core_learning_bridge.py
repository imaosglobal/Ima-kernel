from founder.executive_ai.memory.memory_store import save_memory


def accept_validated_learning(item):

    return save_memory(
        "community_validated_learning",
        item,
        category="community_learning",
        importance=95
    )
