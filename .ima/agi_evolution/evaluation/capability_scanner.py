from pathlib import Path
import json
import time

ROOT=Path(".ima/agi_evolution")

CHECKS={
    "runtime":"ima_master_runtime.py",
    "memory":"conversation_layer.py",
    "brain":"ima_brain.py",
    "learning":"learning/meta_orchestrator.py",
    "agi_orchestrator":"runtime/agi_orchestrator.py",
    "agi_bridge":"runtime/ima_agi_bridge.py",
    "world_model":"world_model",
    "connectors":"connectors",
    "frontend":"ima-ui",
    "android":"android"
}

def scan():
    result={
        "time":time.time(),
        "capabilities":{}
    }

    for name,path in CHECKS.items():
        exists=Path(path).exists() or (ROOT/path).exists()
        result["capabilities"][name]={
            "status":"active" if exists else "missing",
            "path":path
        }

    Path(".ima/agi_evolution/runtime/reality_state.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False)
    )

    return result


if __name__=="__main__":
    print(json.dumps(scan(),indent=2,ensure_ascii=False))
