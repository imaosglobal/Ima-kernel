from learning.learning_memory import load_memory, save_memory
from learning.action_engine import execute_learning_action
from datetime import datetime


def make_learning_decision(area, reason):

    data = load_memory()

    data["decisions"].append({
        "time": str(datetime.now()),
        "decision": area,
        "reason": reason,
        "status": "planned"
    })

    save_memory(data)

    execute_learning_action(
        area,
        reason
    )

    return True
