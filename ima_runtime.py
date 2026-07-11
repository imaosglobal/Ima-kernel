from pathlib import Path
import json
import time
import importlib


ROOT = Path(".")
GOV = ROOT / ".ima" / "governance"


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def check_file(path):
    return {
        "path": str(path),
        "exists": path.exists()
    }


def check_module(module):
    result = {
        "module": module,
        "status": "failed"
    }

    try:
        importlib.import_module(module)
        result["status"] = "ok"
    except Exception as e:
        result["error"] = str(e)

    return result


def runtime_check():
    print("=== IMA CORE RUNTIME ===")

    state = {
        "time": time.time(),
        "system": "IMA",
        "runtime": "v1",
        "checks": {}
    }

    state["checks"]["brain"] = check_module(
        "learning.meta_orchestrator"
    )

    state["checks"]["learning_orchestrator"] = check_module(
        "learning.connect_orchestrator"
    )

    state["checks"]["product_runtime"] = check_file(
        Path("product/product_runtime.py")
    )

    state["checks"]["device_protocol"] = check_file(
        Path("product/device_bridge/device_protocol.json")
    )

    state["checks"]["safety"] = check_file(
        Path("product/safety/safety_policy.json")
    )

    state["checks"]["voice"] = check_file(
        Path("product/voice/voice_pipeline.json")
    )

    active = 0

    for name, result in state["checks"].items():
        print(name, ":", result)

        if result.get("status") == "ok" or result.get("exists"):
            active += 1

    state["active_components"] = active

    GOV.mkdir(parents=True, exist_ok=True)

    (GOV / "runtime_registry.json").write_text(
        json.dumps(
            state,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print()
    print("ACTIVE COMPONENTS:", active)
    print("RUNTIME REGISTRY SAVED")

    return state


if __name__ == "__main__":
    runtime_check()
