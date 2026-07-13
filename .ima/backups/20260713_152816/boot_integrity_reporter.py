import json
import time
import hashlib
from pathlib import Path

REPORT = Path(".ima/runtime/boot_integrity_report.json")

FILES = [
    "IMA_START.py",
    "kernel/runtime/CANONICAL/python_bridge.py",
    ".ima/runtime/memory_bus.py",
    "ima_master_runtime.py",
    "conversation_layer.py",
    "identity_context.py",
    "learning/evolution_controller.py",
]

def create_report(status="ONLINE"):
    data = {
        "status": status,
        "timestamp": time.time(),
        "components": {}
    }

    for f in FILES:
        p = Path(f)
        if p.exists():
            data["components"][f] = {
                "exists": True,
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest()
            }
        else:
            data["components"][f] = {
                "exists": False
            }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    return data
