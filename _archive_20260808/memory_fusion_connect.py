from pathlib import Path
import json
import time
import importlib.util

ROOT = Path(".").resolve()

STATE = ROOT / ".ima/runtime/memory_fusion_state.json"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


memory_bus = load_module(
    "memory_bus",
    ".ima/runtime/memory_bus.py"
)

memory = {
    "status": "ONLINE",
    "connected": [],
    "timestamp": time.time()
}


targets = [
    "conversation_layer.py",
    "identity_context.py",
    "ima_master_runtime.py",
    "learning/evolution_controller.py",
    "kernel/runtime/CANONICAL/python_bridge.py"
]


for t in targets:
    if Path(t).exists():
        memory["connected"].append(t)


event = {
    "type": "MEMORY_FUSION_BOOT",
    "time": time.time(),
    "modules": memory["connected"]
}


try:
    memory_bus.log_event(event)
except Exception:
    pass


STATE.write_text(
    json.dumps(memory, indent=2, ensure_ascii=False)
)

print(json.dumps(memory, indent=2, ensure_ascii=False))
print("[MEMORY FUSION ONLINE]")
