import json
import time
from pathlib import Path

LOG = Path(".ima/brain_sync.jsonl")


def broadcast(event):

    LOG.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(LOG, "a", encoding="utf8") as f:
        f.write(
            json.dumps(
                event,
                ensure_ascii=False
            )
            + "\n"
        )

    results = []

    if event.get("type") == "LEARNING_EVENT":

        chain = [
            (
                "ima_learning_loop",
                "run_ima_learning_loop"
            ),
            (
                "learning_memory_connector",
                "update_learning_memory"
            ),
            (
                "knowledge_expander",
                "expand_knowledge"
            ),
            (
                "meta_orchestrator",
                "run_meta_analysis"
            )
        ]

        for module_name, function_name in chain:
            try:
                module = __import__(
                    "learning." + module_name,
                    fromlist=[function_name]
                )

                fn = getattr(
                    module,
                    function_name
                )

                fn()

                results.append(
                    module_name + ":OK"
                )

            except Exception as e:
                results.append(
                    module_name + ":ERR:" + str(e)
                )

    return results


def status():
    return {
        "bus": "active",
        "time": time.time()
    }
