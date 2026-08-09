from founder.executive_ai.memory.memory_store import save_memory


def process_feedback(action, feedback):

    return {
        "action": action,
        "feedback": feedback,
        "status": "processed"
    }


def learn_from_feedback(action, feedback):

    result = process_feedback(action, feedback)

    save_memory(
        "action_feedback",
        result,
        category="learning",
        importance=80
    )

    return result


# Compatibility layer for restored modules

def learn_from_action(action, feedback=None):

    return learn_from_feedback(
        action,
        feedback or "no_feedback"
    )
