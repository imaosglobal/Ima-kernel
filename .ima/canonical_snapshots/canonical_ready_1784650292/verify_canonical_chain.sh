#!/data/data/com.termux/files/usr/bin/bash
set -e

R=.ima/agi_evolution/runtime

echo "=== CANONICAL CHAIN CHECK ==="

echo "[1] LOCK"
cat $R/CANONICAL_KERNEL_LOCK.json

echo "[2] BOOT GATE"
python3 $R/ima_boot_gate.py

echo "[3] MASTER"
python3 $R/ima_master_runtime.py | head -80

echo "=== CHAIN OK ==="
