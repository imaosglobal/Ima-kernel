from founder.executive_ai.learning_journal.journal_store import get_all


def reflect():

    entries = get_all()

    return {
        "total_memory": len(entries),
        "latest": entries[-10:]
    }
