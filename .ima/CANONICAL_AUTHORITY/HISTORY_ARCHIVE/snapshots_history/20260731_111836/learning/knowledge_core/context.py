
def build_context(question,memory=None):
    return {
        "question":question,
        "memory_used":bool(memory)
    }
