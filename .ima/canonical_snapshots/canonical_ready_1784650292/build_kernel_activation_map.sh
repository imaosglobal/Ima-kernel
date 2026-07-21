#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/ima_kernel"
RUNTIME="$BASE/.ima/agi_evolution/runtime"

echo "=== KERNEL ACTIVATION MAP ==="

echo "[1] SEARCH CANONICAL KERNEL"

find "$BASE" \
-type f \
-name "*.py" \
| grep -E "kernel|mother|runtime|boot" \
| grep -v backups \
| grep -v __pycache__ \
> "$RUNTIME/canonical_kernel_candidates.txt"


echo "[2] SHOW CANDIDATES"

cat "$RUNTIME/canonical_kernel_candidates.txt"


echo
echo "[3] CHECK CLASSES"

grep -R "class Kernel\|class Mother\|def boot\|def run" \
"$BASE/ima" \
"$BASE/.ima/runtime" \
2>/dev/null \
> "$RUNTIME/kernel_activation_functions.txt"


echo
echo "[4] CREATE ACTIVATION REPORT"

python3 <<'PY'
from pathlib import Path
import json,time

root=Path(".ima/agi_evolution/runtime")

files=[
"canonical_kernel_candidates.txt",
"kernel_activation_functions.txt"
]

report={
"time":time.time(),
"stage":"kernel_activation_mapping",
"files":{}
}

for f in files:
    p=root/f
    report["files"][f]=p.exists()

(root/"kernel_activation_report.json").write_text(
json.dumps(report,indent=2)
)

print(json.dumps(report,indent=2))
PY


echo
echo "=== MAP COMPLETE ==="

