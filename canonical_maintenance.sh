#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA CANONICAL MAINTENANCE ==="

mkdir -p .ima/archive_cleanup

echo "[1] REMOVE PYTHON CACHE"
find . -type d -name "__pycache__" -prune -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

echo "[2] REMOVE OLD PID FILES"
find . -type f -name "*.pid" -delete

echo "[3] ARCHIVE OLD DEVELOPMENT FILES"

find . -maxdepth 2 -type f \( \
-name "backup_*" -o \
-name "*_backup_*" -o \
-name "*before*" -o \
-name "*.broken" -o \
-name "*.stable*" \
\) \
! -path "./.ima/archive_cleanup/*" \
-exec mv {} .ima/archive_cleanup/ \; 2>/dev/null || true

echo "[4] LIMIT CHECKPOINT FILES"

mkdir -p .ima/archive_cleanup/checkpoints

find . -maxdepth 1 -type f -name "*checkpoint*.tar.gz" \
-exec mv {} .ima/archive_cleanup/checkpoints/ \; 2>/dev/null || true

echo "[5] SYNC CANONICAL LOCKS"

python3 - <<'PY'
from pathlib import Path
import json,hashlib,time

for name in [
".ima/runtime/canonical_fusion_lock.json",
".ima/runtime/canonical_system_lock.json"
]:
    p=Path(name)
    if not p.exists():
        continue

    data=json.loads(p.read_text())

    for f in data.get("components",{}):
        x=Path(f)
        if x.exists():
            data["components"][f]=hashlib.sha256(
                x.read_bytes()
            ).hexdigest()

    data["timestamp"]=time.time()
    p.write_text(
        json.dumps(data,indent=2,ensure_ascii=False)
    )

print("[LOCKS SYNCED]")
PY

echo "[6] DEPENDENCY AUDIT"

if [ -f canonical_dependency_audit.sh ]; then
    bash canonical_dependency_audit.sh
fi

echo "[7] WRITE REPORT"

python3 - <<'PY'
from pathlib import Path
import json,time

files=sum(1 for x in Path(".").rglob("*") if x.is_file())

Path(".ima/runtime/maintenance_report.json").write_text(
json.dumps({
"status":"OK",
"time":time.time(),
"files":files
},indent=2)
)

print("[REPORT CREATED]")
PY

echo "=== MAINTENANCE COMPLETE ==="
