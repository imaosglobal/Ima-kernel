#!/data/data/com.termux/files/usr/bin/bash

echo "=== WHO IS IMA ==="

echo "ENTRY:"
grep -R '"entry_point"\|"canonical":' .ima/governance 2>/dev/null | grep -E "IMA_START|meta_orchestrator|canonical" | head -3

echo ""
echo "RUNTIME:"
python3 - <<'PY'
from pathlib import Path
import json

p=Path(".ima/runtime/canonical_boot_guard.json")
if p.exists():
 print(json.loads(p.read_text()))
else:
 print("no guard report")
PY

echo ""
echo "LOCK:"
grep state .ima/governance/RELEASE_LOCK.json

echo "=== END ==="
