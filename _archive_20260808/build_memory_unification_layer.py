from pathlib import Path
import json
import time
import hashlib
import subprocess

ROOT = Path(".")
RUNTIME = ROOT / ".ima" / "runtime"

RUNTIME.mkdir(parents=True, exist_ok=True)

target = RUNTIME / "memory_unification_layer.py"

code = r'''
import json
import hashlib
import time
from pathlib import Path

SOURCES = [
    ".ima/memory.json",
    ".ima/conversation_memory.json",
    ".ima/state_memory.json",
    "learning/user_memory.json",
    "learning/world_memory.json",
    "learning/learning_memory.json",
]

STATE = Path(".ima/runtime/memory_unification_state.json")


def file_hash(path):
    p = Path(path)
    if not p.exists():
        return None
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_memory():
    result = {}
    for src in SOURCES:
        try:
            p = Path(src)
            if p.exists():
                with p.open(encoding="utf-8") as f:
                    result[src] = json.load(f)
        except Exception as e:
            result[src] = {"error": str(e)}
    return result


def sync():
    data = load_memory()

    state = {
        "updated": time.time(),
        "sources": {},
        "count": len(data)
    }

    for src in SOURCES:
        state["sources"][src] = {
            "exists": Path(src).exists(),
            "hash": file_hash(src)
        }

    STATE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    return state


def status():
    if not STATE.exists():
        return {"status":"not_initialized"}

    return json.loads(
        STATE.read_text(encoding="utf-8")
    )


if __name__ == "__main__":
'''

target.write_text(code, encoding="utf-8")


r = subprocess.run(
    ["python3", "-m", "py_compile", str(target)],
    capture_output=True,
    text=True
)

if r.returncode:
else:


from importlib.util import spec_from_file_location, module_from_spec

spec = spec_from_file_location(
    "memory_unification_layer",
    target
)

mod = module_from_spec(spec)
spec.loader.exec_module(mod)

result = mod.sync()


