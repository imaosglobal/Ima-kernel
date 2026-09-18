import json
import py_compile
import time
from pathlib import Path
from .model_registry import refresh

STATE = Path(".ima/adaptive_maintenance.json")
TTL = 21600


def scan_code(root=Path(".")):
    checked = 0
    errors = []
    for path in root.rglob("*.py"):
        if any(part in {".git", "node_modules", "__pycache__"} for part in path.parts):
            continue
        try:
            py_compile.compile(str(path), doraise=True)
            checked += 1
        except Exception as e:
            errors.append({"file": str(path), "error": str(e)})
    return {"checked": checked, "errors": errors}


def run(force=False):
    if not force and STATE.exists():
        try:
            old = json.loads(STATE.read_text(encoding="utf8"))
            if time.time() - old.get("time", 0) < TTL:
                return old
        except Exception:
            pass
    result = {"time": time.time(), "code": scan_code(), "models": refresh(force=True)}
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf8")
    return result
