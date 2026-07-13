#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA CANONICAL SUPERVISOR LOCK ==="

mkdir -p .ima/governance
mkdir -p kernel/runtime/CANONICAL

SUP="kernel/runtime/CANONICAL/IMA_SUPERVISOR.py"

if [ -f "$SUP" ]; then
    echo "[OK] Supervisor exists"
else

cat > "$SUP" <<'PY'
#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import time
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[3]
STATE=ROOT/".ima/governance/SUPERVISOR_STATE.json"

CANONICAL="kernel/runtime/CANONICAL/IMA_SUPERVISOR.py"


def digest():
    return hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()


def verify():

    if not STATE.exists():
        return False

    data=json.loads(
        STATE.read_text()
    )

    return (
        data.get("canonical")==CANONICAL
        and data.get("hash")==digest()
    )


def boot():

    if not verify():
        print("[FAIL] SUPERVISOR INTEGRITY")
        return 1

    print("[OK] CANONICAL SUPERVISOR")
    print("[OK] HASH VERIFIED")
    print("[OK] LOCKED")

    return 0


if __name__=="__main__":
    sys.exit(boot())
PY

chmod +x "$SUP"

fi


HASH=$(sha256sum "$SUP" | awk '{print $1}')


cat > .ima/governance/SUPERVISOR_STATE.json <<EOF
{
  "state":"CANONICAL_LOCKED",
  "canonical":"kernel/runtime/CANONICAL/IMA_SUPERVISOR.py",
  "hash":"$HASH",
  "created":$(date +%s),
  "policy":"single_supervisor_only"
}
EOF


cat > .ima/governance/SUPERVISOR_POLICY.json <<'EOF'
{
  "allowed_supervisor":
    "kernel/runtime/CANONICAL/IMA_SUPERVISOR.py",

  "forbidden_patterns":[
    "supervisor.py",
    "SUPERVISOR.js",
    "daemon_supervisor",
    "master_supervisor"
  ],

  "mode":"LOCKED"
}
EOF


echo ""
echo "=== VERIFY LOCK ==="

python3 kernel/runtime/CANONICAL/IMA_SUPERVISOR.py


echo ""
echo "=== SUPERVISOR CANONICAL LOCKED ==="
echo "$SUP"
