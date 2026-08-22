#!/data/data/com.termux/files/usr/bin/bash
set -u

ROOT="$HOME/ima_kernel"
CANON="$ROOT/kernel/runtime/CANONICAL"
REPORT="$ROOT/CANONICAL_REPAIR_REPORT.txt"

echo "=== IMA CANONICAL REPAIR CHECK ===" | tee "$REPORT"
echo "TIME: $(date)" | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

cd "$ROOT" || exit 1

check_file() {
    if [ -f "$1" ]; then
        echo "[OK] $1" | tee -a "$REPORT"
    else
        echo "[MISS] $1" | tee -a "$REPORT"
    fi
}

echo "--- FILE STRUCTURE ---" | tee -a "$REPORT"

check_file "$CANON/IMA_RUNTIME.js"
check_file "$CANON/python_bridge.py"
check_file "$CANON/IMA_STATE.js"
check_file "$CANON/IMA_EVENTS.js"
check_file "$ROOT/IMA_START.py"

echo "" | tee -a "$REPORT"

echo "--- PERMISSIONS FIX ---" | tee -a "$REPORT"

chmod 700 "$CANON" 2>/dev/null || true
chmod 700 "$CANON"/*.py 2>/dev/null || true
chmod 600 "$CANON"/*.js 2>/dev/null || true

echo "[OK] permissions normalized" | tee -a "$REPORT"

echo "" | tee -a "$REPORT"

echo "--- NODE TEST ---" | tee -a "$REPORT"

if node "$CANON/IMA_RUNTIME.js" > /tmp/ima_runtime_output.txt 2>/tmp/ima_runtime_error.txt
then
    echo "[OK] NODE EXECUTION" | tee -a "$REPORT"
    cat /tmp/ima_runtime_output.txt | tee -a "$REPORT"
else
    echo "[FAIL] NODE EXECUTION" | tee -a "$REPORT"
    cat /tmp/ima_runtime_error.txt | tee -a "$REPORT"
fi

echo "" | tee -a "$REPORT"

echo "--- PYTHON BRIDGE TEST ---" | tee -a "$REPORT"

python3 - <<'PY' 2>&1 | tee -a "$REPORT"
import sys
sys.path.insert(0,"kernel/runtime/CANONICAL")

try:
    import python_bridge
except Exception as e:
PY

echo "" | tee -a "$REPORT"

echo "--- START ENTRY TEST ---" | tee -a "$REPORT"

python3 IMA_START.py 2>&1 | tee -a "$REPORT"

echo "" | tee -a "$REPORT"

echo "=== FINISHED ===" | tee -a "$REPORT"
echo "REPORT: $REPORT"
