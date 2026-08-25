from founder.executive_ai.memory.memory_store import (
    save_memory,
    query_memory,
)


def _action_identity(action):
    """
    Canonical action identity.

    Identity is action + target only.
    Score/economics/reasoning are deliberately excluded.
    """
    if not isinstance(action, dict):
        return None

    action_name = action.get("action")
    target = action.get("target")

    if action_name is None or target is None:
        return None

    return (
        str(action_name),
        str(target),
    )


def save_action(action, result, reason):
    """
    Persist an action exactly once per canonical action identity.
    """

    identity = _action_identity(action)

    if identity is not None:
        try:
            existing = query_memory("actions")

            for record in existing:
                if not isinstance(record, dict):
                    continue

                value = record.get("value", record)

                if not isinstance(value, dict):
                    continue

                existing_action = value.get("action")

                if not isinstance(existing_action, dict):
                    continue

                if _action_identity(existing_action) == identity:
                    return record

        except Exception:
            # Memory lookup failure must not break action execution.
            pass

    return save_memory(
        "actions",
        {
            "action": action,
            "result": result,
            "reason": reason,
        },
    )


def get_actions():
    return query_memory("actions")
