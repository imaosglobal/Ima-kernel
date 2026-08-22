#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

mkdir -p .ima/runtime

REPORT=".ima/runtime/dependency_registry.json"
LOCK=".ima/runtime/canonical_fusion_lock.json"

echo "=== IMA CANONICAL DEPENDENCY AUDIT ==="

python3 - <<'PY'
from pathlib import Path
import json,time,hashlib

root=Path(".")
ignore={
".git",
"node_modules",
"__pycache__",
".ima/archive_cleanup"
}

files={}

for p in root.rglob("*"):
    if not p.is_file():
        continue

    if any(x in p.parts for x in ignore):
        continue

    try:
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        files[str(p)]={
            "sha256":h,
            "size":p.stat().st_size
        }
    except:
        pass

data={
    "status":"AUDIT_ACTIVE",
    "timestamp":time.time(),
    "files":files,
    "count":len(files)
}

Path(".ima/runtime/dependency_registry.json").write_text(
    json.dumps(data,indent=2,ensure_ascii=False)
)

PY


if [ -f "$LOCK" ]; then
echo "[OK] CANONICAL LOCK EXISTS"
else
echo "[WARN] NO CANONICAL LOCK"
fi


echo "=== DEPENDENCY AUDIT COMPLETE ==="

