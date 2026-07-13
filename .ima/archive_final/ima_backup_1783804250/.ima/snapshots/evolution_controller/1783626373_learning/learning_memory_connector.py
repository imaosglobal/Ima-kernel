from learning.learning_memory import store_pattern, store_evaluation
from learning.ima_awareness import ima_awareness


def update_learning_memory():

    awareness = ima_awareness()

    store_pattern(
        str(awareness["observations"])
    )

    for item in awareness["pending_improvements"]:
        store_evaluation(
            item,
            0.5,
            "ממתין לשיפור"
        )

    return {
        "status": "learning memory updated",
        "patterns": len(awareness["observations"]),
        "improvements": len(awareness["pending_improvements"])
    }
