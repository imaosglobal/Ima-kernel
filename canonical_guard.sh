#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
CANON="$ROOT/kernel/runtime/CANONICAL"

cd "$ROOT"

echo "=== IMA CANONICAL GUARD ==="
echo "[IMA] root=$ROOT"

FAIL=0

check_file() {
  if [ -f "$1" ]; then
    echo "[OK] $1"
  else
    echo "[FAIL] missing: $1"
    FAIL=1
  fi
}

echo "[1] VERIFY CANONICAL COMPONENTS"

REQUIRED=(
  "IMA_CANONICAL_VISION.md"
  "kernel/runtime/CANONICAL/IMA_RUNTIME.js"
  "kernel/runtime/CANONICAL/IMA_POLICY.js"
  "kernel/runtime/CANONICAL/IMA_CORE_CONTRACT.js"
  "kernel/runtime/CANONICAL/IMA_SYSTEM_INTEGRITY.js"
  "kernel/runtime/CANONICAL/IMA_PRESERVATION_VERIFY.js"
  "kernel/runtime/CANONICAL/IMA_DERIVATION_REGISTRY.js"
  "kernel/runtime/CANONICAL/memory/IMA_MEMORY.js"
  "kernel/runtime/CANONICAL/gateway/IMA_MODEL_GATEWAY.js"
  "kernel/runtime/CANONICAL/gateway/IMA_TOOL_GATEWAY.js"
  "kernel/runtime/CANONICAL/gateway/IMA_AGENT_GATEWAY.js"
  "kernel/runtime/CANONICAL/orchestration/IMA_ACTION_ENGINE.js
  kernel/runtime/CANONICAL/IMA_SELF_HOSTED.js"
)

for f in "${REQUIRED[@]}"; do
  check_file "$f"
done

if [ "$FAIL" -ne 0 ]; then
  echo "[FAIL] required components missing"
  exit 1
fi

echo "[2] VERIFY SHA-256"

python3 - <<'PY'
from pathlib import Path
import hashlib

root = Path(".")
files = [
    "IMA_CANONICAL_VISION.md",
    "kernel/runtime/CANONICAL/IMA_CORE_CONTRACT.js",
    "kernel/runtime/CANONICAL/IMA_SYSTEM_INTEGRITY.js",
    "kernel/runtime/CANONICAL/IMA_PRESERVATION_VERIFY.js",
    "kernel/runtime/CANONICAL/IMA_DERIVATION_REGISTRY.js",
    "kernel/runtime/CANONICAL/memory/IMA_MEMORY.js",
    "kernel/runtime/CANONICAL/gateway/IMA_MODEL_GATEWAY.js",
    "kernel/runtime/CANONICAL/gateway/IMA_TOOL_GATEWAY.js",
    "kernel/runtime/CANONICAL/gateway/IMA_AGENT_GATEWAY.js",
    "kernel/runtime/CANONICAL/orchestration/IMA_ACTION_ENGINE.js
  kernel/runtime/CANONICAL/IMA_SELF_HOSTED.js",
]

for name in files:
    p = root / name
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    print(f"[OK] SHA256 {name} {digest}")
PY

echo "[3] VERIFY SYSTEM INTEGRITY"

node "$CANON/IMA_SYSTEM_INTEGRITY.js"

echo "[4] VERIFY CORE TEST"

npm test

echo "[5] VERIFY GIT SAFETY"

if git diff --check; then
  echo "[OK] GIT DIFF CHECK"
else
  echo "[FAIL] GIT DIFF CHECK"
  exit 1
fi

echo "[6] VERIFY WORKTREE"

git status --short

echo "=== IMA CANONICAL STATE VERIFIED ==="
echo "CANONICAL_GUARD=PASS"
