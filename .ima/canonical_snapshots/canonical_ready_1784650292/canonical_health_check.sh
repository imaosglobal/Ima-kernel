#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_kernel || exit 1

LOG=".ima/runtime/ima_health.log"

echo "=== IMA HEALTH CHECK ==="

python3 IMA_START.py > "$LOG" 2>&1

if grep -q "IMA SYSTEM READY" "$LOG"; then
    echo "[OK] IMA HEALTHY"
else
    echo "[FAIL] IMA FAILED"
    cat "$LOG"
fi
