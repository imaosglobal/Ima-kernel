from founder.executive_ai.memory.memory_store import save_memory


def sync_lesson(lesson):

    return save_memory(
        "community_lesson",
        lesson,
        category="validated_learning",
        importance=90
    )
