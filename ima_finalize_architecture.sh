#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA FINAL ARCHITECTURE FREEZE ==="

mkdir -p .ima/governance

echo "[1] Creating canonical architecture map"

cat > .ima/governance/canonical_map.json <<JSON
{
  "system": "IMA",
  "state": "FROZEN",
  "brain": "learning/meta_orchestrator.py",
  "orchestrator": "learning/meta_orchestrator.py",
  "connectors": [
    "learning/module_registry.py"
  ],
  "policy": [
    "single_brain_only",
    "single_orchestrator_only",
    "connectors_allowed",
    "block_duplicate_brain_creation",
    "redirect_to_canonical_path"
  ]
}
JSON


echo "[2] Updating brain guard"

cat > learning/brain_guard.py <<'PY'
from pathlib import Path
import json

CANONICAL_BRAIN = Path("learning/meta_orchestrator.py")
CANONICAL_ORCHESTRATOR = Path("learning/meta_orchestrator.py")

CONNECTORS = [
    Path("learning/module_registry.py")
]

REGISTRY = Path(".ima/governance/brain_registry.json")


def create_registry():

    data = {
        "system": "IMA",
        "state": "LOCKED",
        "brain": str(CANONICAL_BRAIN),
        "orchestrator": str(CANONICAL_ORCHESTRATOR),
        "connectors": [str(x) for x in CONNECTORS],
        "policy": [
            "single_brain_only",
            "single_orchestrator_only",
            "connectors_allowed",
            "block_duplicate_creation"
        ]
    }

    REGISTRY.parent.mkdir(parents=True, exist_ok=True)

    REGISTRY.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


def verify_brain(path):

    p = Path(path)

    if p == CANONICAL_BRAIN:
        return True

    if p in CONNECTORS:
        return True

    if "orchestrator" in p.name.lower():
        raise RuntimeError(
            "IMA BLOCKED duplicate orchestrator. USE: learning/meta_orchestrator.py"
        )

    return True


if __name__ == "__main__":
    create_registry()
PY


echo "[3] Rebuilding governance registry"

python3 learning/brain_guard.py


echo "[4] Testing brain"

python3 - <<'PY'
from learning.brain_guard import verify_brain

verify_brain("learning/meta_orchestrator.py")
verify_brain("learning/module_registry.py")

PY


echo "[5] Testing learning modules"

python3 - <<'PY'
from pathlib import Path
import importlib

ok=0
fail=0

for f in Path("learning").glob("*.py"):
    if f.name.startswith("_"):
        continue

    try:
        importlib.import_module("learning."+f.stem)
        ok+=1
    except Exception as e:
        fail+=1


if fail:
    raise SystemExit(1)
PY


echo "[6] Full system check"

python3 ima_full_system_check.py


echo "[7] Git freeze"

git add \
.ima/governance/canonical_map.json \
.ima/governance/brain_registry.json \
learning/brain_guard.py

git commit -m "IMA canonical architecture freeze" || true

git tag -a IMA_PRODUCT_BASELINE_v1 \
-m "IMA product baseline architecture frozen" || true


echo "[8] Final status"

git status

echo
echo "=== IMA FINAL ARCHITECTURE COMPLETE ==="
