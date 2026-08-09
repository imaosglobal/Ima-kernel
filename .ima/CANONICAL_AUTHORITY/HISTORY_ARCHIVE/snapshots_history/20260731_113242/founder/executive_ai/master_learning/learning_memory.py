from founder.executive_ai.memory.memory_store import save_memory


def remember(key,value):

    return save_memory(
        key,
        value,
        category="learning",
        importance=80
    )
