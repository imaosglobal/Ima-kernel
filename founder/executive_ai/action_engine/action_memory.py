
from founder.executive_ai.memory.memory_store import (
    save_memory,
    query_memory
)


def save_action(action,result,reason):

    return save_memory(
        "actions",
        {
            "action": action,
            "result": result,
            "reason": reason
        }
    )


def get_actions():

    return query_memory(
        "actions"
    )
