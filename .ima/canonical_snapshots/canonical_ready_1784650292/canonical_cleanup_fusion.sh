#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA CANONICAL CLEANUP FUSION ==="

STAMP=$(date +%s)

echo "[1] FULL SAFETY BACKUP"

tar -czf "ima_before_cleanup_${STAMP}.tar.gz" \
IMA_START.py \
kernel/runtime/CANONICAL \
.ima/runtime \
ima_master_runtime.py \
conversation_layer.py \
identity_context.py \
learning/evolution_controller.py \
api_boot_connector.py \
canonical_boot_guard.py \
boot_integrity_reporter.py \
2>/dev/null || true


echo "[2] CREATE ARCHIVE AREA"

mkdir -p .ima/archive_cleanup


echo "[3] MOVE OLD BACKUPS"

find . -maxdepth 1 -type f \
-name "backup_before_*" \
-exec mv {} .ima/archive_cleanup/ \;

find . -maxdepth 1 -type f \
-name "IMA_START.py.before*" \
-exec mv {} .ima/archive_cleanup/ \;

find . -maxdepth 1 -type f \
-name "*broken*" \
-exec mv {} .ima/archive_cleanup/ \;


echo "[4] CREATE CANONICAL MAP"

python3 - <<'PY'
from pathlib import Path
import json,time,hashlib

files=[
"IMA_START.py",
"api_boot_connector.py",
"canonical_boot_guard.py",
"boot_integrity_reporter.py",
"kernel/runtime/CANONICAL/python_bridge.py",
".ima/runtime/memory_bus.py",
"ima_master_runtime.py",
"conversation_layer.py",
"identity_context.py",
"learning/evolution_controller.py"
]

data={
"status":"CANONICAL_FUSED",
"time":time.time(),
"entry":"IMA_START.py",
"components":{}
}

for f in files:
    p=Path(f)
    if p.exists():
        data["components"][f]=hashlib.sha256(
            p.read_bytes()
        ).hexdigest()

Path(".ima/runtime/canonical_fusion_lock.json").write_text(
json.dumps(data,indent=2,ensure_ascii=False)
)

print("[LOCK CREATED]",len(data["components"]))
PY


echo "[5] COMPILE TEST"

python3 -m py_compile \
IMA_START.py \
api_boot_connector.py \
canonical_boot_guard.py \
boot_integrity_reporter.py


echo "[6] BOOT TEST"

python3 IMA_START.py


echo "[7] HEALTH TEST"

curl -s http://127.0.0.1:8080/health || true


echo "=== CLEANUP COMPLETE ==="

