#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== IMA FINAL CANONICAL LOCK ==="

ROOT="$HOME/ima_kernel"

BRAIN="learning/meta_orchestrator.py"
ORCH="learning/meta_orchestrator.py"

mkdir -p .ima/governance

cat > .ima/governance/creation_policy.json <<EOF
{
  "system": "IMA",
  "state": "LOCKED",
  "brain": "$BRAIN",
  "orchestrator": "$ORCH",
  "policy": [
    "single_brain_only",
    "single_orchestrator_only",
    "block_duplicate_creation",
    "redirect_to_canonical_path",
    "no_new_kernel_creation"
  ],
  "redirect": {
    "brain": "$BRAIN",
    "orchestrator": "$ORCH"
  }
}
EOF

python3 - <<'PY'
from pathlib import Path
import json

policy=json.loads(Path(".ima/governance/creation_policy.json").read_text())

print("BRAIN:", policy["brain"])
print("ORCHESTRATOR:", policy["orchestrator"])

assert Path(policy["brain"]).exists()
assert Path(policy["orchestrator"]).exists()

print("CANONICAL LOCK OK")
PY

python3 - <<'PY'
from learning.brain_guard import verify_brain

verify_brain("learning/meta_orchestrator.py")

print("BRAIN GUARD OK")
PY

python3 ima_full_system_check.py

git add .ima/governance/creation_policy.json

git commit -m "IMA canonical architecture locked"

git tag -a IMA_KERNEL_CANONICAL_LOCK_v1 \
-m "Single brain single orchestrator architecture locked" || true

echo "=== IMA CANONICAL LOCK COMPLETE ==="
