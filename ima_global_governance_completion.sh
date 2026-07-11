#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA GLOBAL GOVERNANCE COMPLETION ==="

mkdir -p \
.ima/governance \
product/runtime \
users \
memory \
safety \
devices/mobile \
devices/android \
devices/robot \
devices/iot \
devices/space \
deployment

echo "[1] Verify canonical brain"

python3 - <<'PY'
from learning.brain_guard import verify_brain
verify_brain("learning/meta_orchestrator.py")
print("CANONICAL BRAIN OK")
PY


echo "[2] Create product layer"

cat > product/runtime/README.md <<'EOF'
IMA PRODUCT RUNTIME

Single entry layer between users/devices and IMA brain.

Flow:

DEVICE
  |
PRODUCT RUNTIME
  |
META ORCHESTRATOR
  |
KERNEL
EOF


echo "[3] Create user layer"

cat > users/user_model.json <<'EOF'
{
 "system":"IMA",
 "profiles":[
  "child",
  "family",
  "adult"
 ],
 "permissions":"governed"
}
EOF


echo "[4] Create memory layer"

cat > memory/memory_policy.json <<'EOF'
{
 "system":"IMA",
 "memory_types":[
  "personal",
  "learning",
  "system"
 ],
 "policy":[
  "privacy_first",
  "deduplicate",
  "controlled_learning"
 ]
}
EOF


echo "[5] Create safety layer"

cat > safety/safety_policy.json <<'EOF'
{
 "system":"IMA",
 "guards":[
  "child_guard",
  "privacy_guard",
  "emotional_safety",
  "parent_control"
 ]
}
EOF


echo "[6] Create device registry"

cat > devices/device_registry.json <<'EOF'
{
 "system":"IMA",
 "supported_layers":[
  "mobile",
  "android",
  "robot",
  "iot",
  "space"
 ],
 "gateway":"product/runtime"
}
EOF


echo "[7] Create deployment layer"

cat > deployment/deployment_registry.json <<'EOF'
{
 "system":"IMA",
 "targets":[
  "mobile",
  "cloud",
  "robotics",
  "embedded"
 ]
}
EOF


echo "[8] Connect orchestrator registry"

python3 - <<'PY'
import json,time
from pathlib import Path

p=Path(".ima/governance/orchestrator_master_registry.json")

data={
"system":"IMA",
"brain":"learning/meta_orchestrator.py",
"canonical_orchestrator":"learning/meta_orchestrator.py",
"connected_orchestrators":[
 "learning/meta_orchestrator.py",
 "learning/connect_orchestrator.py",
 "kernel/runtime/KERNEL_POLICY_ORCHESTRATOR_V3.js"
],
"policy":[
"single_brain_only",
"single_orchestrator_only",
"block_duplicate_creation",
"redirect_to_canonical_path"
],
"locked_at":time.time()
}

p.write_text(
json.dumps(data,ensure_ascii=False,indent=2),
encoding="utf-8"
)

print("ORCHESTRATOR MASTER REGISTRY CREATED")
PY


echo "[9] Create final governance lock"

cat > .ima/governance/final_governance_lock.json <<EOF
{
 "system":"IMA",
 "state":"LOCKED",
 "brain":"learning/meta_orchestrator.py",
 "orchestrator":"learning/meta_orchestrator.py",
 "forbidden_duplicates":[
  "new_brain",
  "new_orchestrator",
  "new_kernel"
 ],
 "redirect":"learning/meta_orchestrator.py"
}
EOF


echo "[10] Verification"

python3 learning/connect_orchestrator.py
python3 ima_full_system_check.py


echo "[11] Git"

git add .
git commit -m "IMA global governance completion and product layer integration" || true

git tag -a IMA_GLOBAL_GOVERNANCE_LOCKED_v1 \
-m "IMA single brain orchestrator product governance locked" || true


echo "=== IMA COMPLETE ==="

git status
git tag --list | grep IMA
