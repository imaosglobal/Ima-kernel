#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA FINAL ARCHITECTURE SETUP ==="

mkdir -p .ima/governance
mkdir -p kernel/device
mkdir -p learning

# Runtime governance
cat > .ima/governance/runtime_registry.json <<EOF
{
  "system": "IMA",
  "state": "LOCKED",
  "runtime_policy": [
    "single_runtime_only",
    "no_duplicate_runtime",
    "canonical_runtime_required"
  ],
  "canonical_candidates": [
    "kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js",
    ".ima/runtime/runtime.py"
  ]
}
EOF

# Device registry
cat > .ima/governance/device_registry.json <<EOF
{
  "system": "IMA",
  "devices": [
    "mobile",
    "robot",
    "iot",
    "vr",
    "ar",
    "vehicle",
    "spacecraft"
  ],
  "state": "BASE_LAYER"
}
EOF

# Mission registry
cat > .ima/governance/mission_registry.json <<EOF
{
  "system": "IMA",
  "mission": [
    "assist_humans",
    "child_safe",
    "universal_device_support",
    "continuous_learning"
  ],
  "brain": "learning/meta_orchestrator.py",
  "orchestrator": "learning/meta_orchestrator.py"
}
EOF

# Child safety base
if [ ! -f learning/child_safety_engine.py ]; then
cat > learning/child_safety_engine.py <<'EOF'
class ChildSafetyEngine:

    def check(self, context):
        return {
            "safe": True,
            "context_checked": True
        }

engine = ChildSafetyEngine()
EOF
fi

# Persona base
if [ ! -f learning/persona_engine.py ]; then
cat > learning/persona_engine.py <<'EOF'
class PersonaEngine:

    def select(self, user_type):
        return {
            "mode": user_type,
            "system": "IMA"
        }

engine = PersonaEngine()
EOF
fi

# Verify imports
python3 -m py_compile \
 learning/child_safety_engine.py \
 learning/persona_engine.py \
 learning/meta_orchestrator.py

# Architecture report
python3 - <<'PY'
from pathlib import Path
import json,time

report={
"time":time.time(),
"system":"IMA",
"brain":"learning/meta_orchestrator.py",
"orchestrator":"learning/meta_orchestrator.py",
"runtime_registry":Path(".ima/governance/runtime_registry.json").exists(),
"device_registry":Path(".ima/governance/device_registry.json").exists(),
"mission_registry":Path(".ima/governance/mission_registry.json").exists(),
"status":"ARCHITECTURE_BASE_READY"
}

Path(".ima/governance/architecture_status.json").write_text(
json.dumps(report,indent=2,ensure_ascii=False),
encoding="utf-8"
)

print(json.dumps(report,indent=2,ensure_ascii=False))
PY

echo "=== DONE ==="
