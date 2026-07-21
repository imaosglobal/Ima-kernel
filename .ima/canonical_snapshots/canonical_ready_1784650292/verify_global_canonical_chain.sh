#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== GLOBAL CANONICAL VERIFICATION ==="

python3 canonical_admission_guard.py kernel/runtime/CANONICAL/python_bridge.py

python3 canonical_admission_guard.py .ima/agi_evolution/runtime/ima_boot_gate.py

python3 canonical_admission_guard.py .ima/agi_evolution/runtime/ima_master_runtime.py

python3 canonical_admission_guard.py IMA_START_SINGLE_ENTRY.py

./ima_canonical_run.sh python3 IMA_START_SINGLE_ENTRY.py > logs/global_chain_test.log 2>&1

grep -E "GLOBAL|POLICY|HASH|FALLBACK|REGISTRY|KERNEL|COMPLETE" logs/global_chain_test.log

echo "=== GLOBAL CANONICAL CHAIN VERIFIED ==="
