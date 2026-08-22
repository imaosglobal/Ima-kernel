#!/data/data/com.termux/files/usr/bin/bash

echo "=== IMA IDENTITY SCAN ==="

echo ""
echo "[ENTRY]"
grep -R '"entry_point"\|"canonical"' .ima/governance/*.json 2>/dev/null | head -5

echo ""
echo "[RUNTIME]"
python3 - <<'PY'
import sys
sys.path.insert(0,"kernel/runtime/CANONICAL")
from python_bridge import boot_runtime
PY

echo ""
echo "[LOCK]"
python3 - <<'PY'
import json
from pathlib import Path

for f in [
".ima/governance/RELEASE_LOCK.json",
".ima/runtime/canonical_system_lock.json"
]:
    p=Path(f)
    if p.exists():
        data=json.loads(p.read_text())
        if "state" in data:
PY

echo ""
echo "[STATUS]"
git status --short | head -5

echo ""
echo "=== END ==="
