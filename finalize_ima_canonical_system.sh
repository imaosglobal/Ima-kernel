#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== IMA CANONICAL FINALIZATION ==="

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "[1] Creating architecture map"

find . \
  -maxdepth 4 \
  \( -name "*.py" -o -name "*.js" -o -name "*.json" \) \
  | sort > ima_full_file_map.txt


echo "[2] Checking orchestrators"

ORCH=$(find learning kernel -iname "*orchestrator*.py" 2>/dev/null || true)

echo "$ORCH"

COUNT=$(echo "$ORCH" | grep -c . || true)

if [ "$COUNT" -gt 2 ]; then
    echo "WARNING: multiple orchestrator candidates"
fi


echo "[3] Checking canonical brain"

python3 - <<'PY'
from pathlib import Path
import json

registry=Path(".ima/governance/brain_registry.json")

if registry.exists():
    data=json.loads(registry.read_text())
else:
PY


echo "[4] Updating runtime registry"

python3 - <<'PY'
from pathlib import Path
import json,time

files=[]

for p in Path(".").rglob("*"):
    if p.suffix in [".py",".js"]:
        files.append(str(p))

data={
    "system":"IMA",
    "state":"CANONICAL",
    "runtime_locked":True,
    "timestamp":time.time(),
    "files":len(files),
    "canonical_brain":"learning/meta_orchestrator.py",
    "canonical_root":"~/ima_kernel"
}

Path(".ima/governance/runtime_registry.json").parent.mkdir(
    parents=True,
    exist_ok=True
)

Path(".ima/governance/runtime_registry.json").write_text(
    json.dumps(data,indent=2,ensure_ascii=False),
    encoding="utf-8"
)

PY


echo "[5] Compile check"

python3 -m compileall learning kernel >/dev/null


echo "[6] Existing system check"

if [ -f ima_full_system_check.py ]; then
    python3 ima_full_system_check.py
fi


echo "[7] Git checkpoint"

git add .

git commit -m "IMA canonical architecture finalization"

git tag -a IMA_KERNEL_CANONICAL_ARCHITECTURE_LOCKED_v1 \
-m "IMA canonical architecture locked"

echo "=== IMA FINALIZED ==="

git status

