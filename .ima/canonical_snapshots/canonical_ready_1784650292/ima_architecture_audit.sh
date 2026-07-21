#!/data/data/com.termux/files/usr/bin/bash

set -u

ROOT="$HOME/ima_kernel"
cd "$ROOT" || exit 1

REPORT=".ima/governance/architecture_audit_report.txt"

mkdir -p .ima/governance

echo "=== IMA CANONICAL ARCHITECTURE AUDIT ===" | tee "$REPORT"
echo "TIME: $(date)" | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

echo "=== COMPONENTS ===" | tee -a "$REPORT"

FILES="
kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js
kernel/runtime/KERNEL_EVENT_BUS.js
kernel/runtime/KERNEL_API_GATEWAY.js
learning/safe_scheduler.py
kernel/device
kernel/plugins
learning/meta_orchestrator.py
learning/persona_engine.py
learning/child_safety_engine.py
learning/single_gate.py
learning/brain_guard.py
"

for f in $FILES
do
    if [ -e "$f" ]; then
        echo "OK   $f" | tee -a "$REPORT"
    else
        echo "MISS $f" | tee -a "$REPORT"
    fi
done


echo "" | tee -a "$REPORT"
echo "=== GOVERNANCE ===" | tee -a "$REPORT"

for f in \
.ima/governance/brain_registry.json \
.ima/governance/runtime_registry.json \
.ima/governance/device_registry.json \
.ima/governance/architecture_status.json
do
    if [ -e "$f" ]; then
        echo "OK   $f" | tee -a "$REPORT"
    else
        echo "MISS $f" | tee -a "$REPORT"
    fi
done


echo "" | tee -a "$REPORT"
echo "=== BRAIN CONNECTION ===" | tee -a "$REPORT"

grep -R "meta_orchestrator" kernel/runtime learning -n 2>/dev/null \
| tee -a "$REPORT"


echo "" | tee -a "$REPORT"
echo "=== EVENT BUS CONNECTION ===" | tee -a "$REPORT"

grep -R "KERNEL_EVENT_BUS\|event_bus\|publish\|subscribe" kernel learning -n 2>/dev/null \
| tee -a "$REPORT"


echo "" | tee -a "$REPORT"
echo "=== API CONNECTION ===" | tee -a "$REPORT"

grep -R "KERNEL_API_GATEWAY\|api" kernel/runtime learning -n 2>/dev/null \
| tee -a "$REPORT"


echo "" | tee -a "$REPORT"
echo "=== SYSTEM TESTS ===" | tee -a "$REPORT"

python3 learning/single_gate.py 2>&1 | tee -a "$REPORT"

python3 learning/evolution_controller.py 2>&1 | tee -a "$REPORT"

python3 ima_full_system_check.py 2>&1 | tee -a "$REPORT"


echo "" | tee -a "$REPORT"
echo "=== GIT STATE ===" | tee -a "$REPORT"

git status | tee -a "$REPORT"

git log -3 --oneline | tee -a "$REPORT"

echo "" | tee -a "$REPORT"
echo "REPORT SAVED:"
echo "$REPORT"

