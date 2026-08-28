from founder.executive_ai.memory.memory_store import (
    save_memory,
    query_memory,
)


def save_action(action, result=None, reason=None):
    payload = {
        "action": action,
        "target": action.get("target") if isinstance(action, dict) else None,
        "result": result,
        "reason": reason,
    }

    return save_memory(
        "actions",
        payload,
    )


def get_actions():

    result = query_memory("actions")

    if not isinstance(result, list):
        return []

    return result
