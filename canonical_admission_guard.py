from pathlib import Path
import json, hashlib, sys

REG=Path(".ima/agi_evolution/runtime/CANONICAL_REGISTRY.json")

def load_registry():
    if not REG.exists():
        raise SystemExit("CANONICAL REGISTRY MISSING")
    return json.loads(REG.read_text())

def verify_component(path):
    reg=load_registry()

    allowed={
        item["file"]:item["sha256"]
        for item in reg.get("allowed_components",[])
    }

    f=str(Path(path))

    if f not in allowed:
        return False

    current=hashlib.sha256(Path(f).read_bytes()).hexdigest()

    if current != allowed[f]:
        return False

    return True

if __name__=="__main__":
    if len(sys.argv)<2:
        raise SystemExit("Usage: canonical_admission_guard.py <file>")

    if not verify_component(sys.argv[1]):
        sys.exit(1)
