#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA BODY LAYER AUDIT ==="

mkdir -p .ima/governance

echo
echo "[1] Searching service layer"

SERVICE=$(find . \
-path "./.git" -prune -o \
-path "./.ima/snapshots" -prune -o \
-type f \
\( -iname "*service*" -o -iname "*gateway*" -o -iname "*server*" \) \
-print | head -20)

echo "$SERVICE"


echo
echo "[2] Searching context layer"

CONTEXT=$(find . \
-path "./.git" -prune -o \
-path "./.ima/snapshots" -prune -o \
-type f \
\( -iname "*context*" -o -iname "*memory_bus*" -o -iname "*state*" \) \
-print | head -20)

echo "$CONTEXT"


echo
echo "[3] Searching device layer"

DEVICE=$(find . \
-path "./.git" -prune -o \
-path "./.ima/snapshots" -prune -o \
-type f \
\( -iname "*device*" -o -iname "*iot*" -o -iname "*bluetooth*" \) \
-print | head -20)

echo "$DEVICE"


echo
echo "[4] Creating canonical body registry"

python3 - <<'PY'
import json
import time
from pathlib import Path


def find_first(patterns):
    root=Path(".")
    results=[]

    for p in root.rglob("*"):
        if not p.is_file():
            continue

        s=str(p).lower()

        if ".git" in s or ".ima/snapshots" in s:
            continue

        for x in patterns:
            if x in s:
                results.append(str(p))
                break

    return results[:10]


registry={

"system":"IMA",

"state":"BODY_LAYER_DISCOVERY",

"brain":
"learning/meta_orchestrator.py",

"orchestrator":
"learning/module_registry.py",

"runtime":
"kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js",

"event_bus":
"kernel/runtime/KERNEL_EVENT_BUS_V2.js",

"api_gateway":
"kernel/runtime/KERNEL_API_GATEWAY_V3.js",

"service_candidates":
find_first([
"service",
"server",
"gateway"
]),

"context_candidates":
find_first([
"context",
"memory_bus",
"state"
]),

"device_candidates":
find_first([
"device",
"iot",
"bluetooth"
]),

"time":
time.time()

}


Path(
".ima/governance/body_layer_registry.json"
).write_text(
json.dumps(
registry,
indent=2,
ensure_ascii=False
),
encoding="utf-8"
)



PY


echo
echo "[5] Runtime connection check"

grep -R \
"require('./KERNEL_EVENT_BUS_V2')" \
kernel/runtime \
>/dev/null && \
echo "EVENT BUS CONNECTED" || \
echo "EVENT BUS UNKNOWN"


echo
echo "[6] Final report"

cat > .ima/governance/body_layer_report.json <<EOF
{
 "system":"IMA",
 "status":"BODY_LAYER_AUDIT_COMPLETE",
 "next":"service_context_device_integration",
 "time":"$(date)"
}
EOF


echo
echo "=== IMA BODY LAYER AUDIT COMPLETE ==="

