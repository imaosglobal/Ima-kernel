import json
import time
from pathlib import Path

def run_snapshot():

    snapshot = {
        "identity": "IMA SYSTEM SNAPSHOT",
        "timestamp": time.time(),
        "layers": {}
    }

    try:
        import ima_fusion_runtime
        snapshot["layers"]["fusion"] = ima_fusion_runtime.fusion_status()
    except Exception as e:
        snapshot["layers"]["fusion"] = {
            "error": str(e)
        }

    try:
        from ima_integration_status import integration_status
        snapshot["layers"]["integration"] = integration_status()
    except Exception as e:
        snapshot["layers"]["integration"] = {
            "error": str(e)
        }

    try:
        import learning.meta_orchestrator
        snapshot["layers"]["learning"] = {
            "connected": True
        }
    except Exception as e:
        snapshot["layers"]["learning"] = {
            "connected": False,
            "error": str(e)
        }

    Path(".ima/ima_system_snapshot.json").write_text(
        json.dumps(
            snapshot,
            ensure_ascii=False,
            indent=2,
            default=str
        )
    )

    return snapshot


if __name__ == "__main__":
    print(json.dumps(
        run_snapshot(),
        ensure_ascii=False,
        indent=2,
        default=str
    ))
