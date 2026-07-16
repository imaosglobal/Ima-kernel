from pathlib import Path
import importlib
import json
import time


MODULES = [
    "health_check",
    "ima_learning_loop",
    "learning_memory_connector",
    "knowledge_dedup",
    "knowledge_expander",
    "improvement_engine",
    "evaluation_engine",
    "feedback_engine",
    "safety_gate",
    "system_introspection",
    "meta_orchestrator",
]


ROOT = Path(".")


def check_module(name):

    result = {
        "module": name,
        "status": "failed",
        "loaded": False
    }

    try:
        importlib.import_module(
            f"learning.{name}"
        )

        result["status"] = "ok"
        result["loaded"] = True

    except Exception as e:
        result["error"] = str(e)

    return result


def build_registry():

    print("=== IMA ORCHESTRATOR CONNECT ===")

    registry = {
        "time": time.time(),
        "system": "IMA",
        "type": "learning_orchestrator_registry",
        "modules": []
    }

    for module in MODULES:
        check = check_module(module)
        registry["modules"].append(check)

        print(
            module,
            ":", 
            check["status"]
        )

    registry["active_modules"] = len(
        [
            x for x in registry["modules"]
            if x["status"] == "ok"
        ]
    )

    Path(
        ".ima/governance/orchestrator_registry.json"
    ).write_text(
        json.dumps(
            registry,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print(
        "ACTIVE:",
        registry["active_modules"]
    )

    print(
        "ORCHESTRATOR REGISTRY SAVED"
    )

    return registry


if __name__ == "__main__":
    build_registry()
