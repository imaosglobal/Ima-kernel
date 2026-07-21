#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/ima_kernel"
RUNTIME="$BASE/.ima/agi_evolution/runtime"

echo "=== IMA MASTER CONNECTION CHECK ==="

echo "[1] MASTER REGISTRY"
cat "$RUNTIME/IMA_MASTER_REGISTRY.json"

echo
echo "[2] BRIDGE STATE"
cat "$RUNTIME/agi_bridge_state.json"

echo
echo "[3] ENTRY POINTS"
cat "$RUNTIME/kernel_entry_scan.txt"

echo
echo "[4] FUNCTION MAP"
head -100 "$RUNTIME/kernel_functions_scan.txt"

echo
echo "[5] PYTHON HEALTH"

python3 -m py_compile \
"$RUNTIME/ima_agi_bridge.py" \
"$RUNTIME/ima_master_runtime.py" \
"$RUNTIME/brain_controller.py" \
"$RUNTIME/decision_engine.py"

echo
echo "[6] CRON"
crontab -l | grep ima

echo
echo "=== CHECK COMPLETE ==="
