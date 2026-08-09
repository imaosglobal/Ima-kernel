from learning.learning_memory import load_memory, save_memory
from datetime import datetime


def evaluate_action(action, result, score):

    data = load_memory()

    data.setdefault("evaluations", [])

    data["evaluations"].append({
        "time": str(datetime.now()),
        "action": action,
        "result": result,
        "score": score
    })

    save_memory(data)

    return {
        "action": action,
        "score": score,
        "status": "evaluated"
    }


def get_evaluations():

    data = load_memory()

    return data.get("evaluations", [])
