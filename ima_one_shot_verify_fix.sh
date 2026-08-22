#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA ONE SHOT VERIFY + FIX ==="

echo "[1] Checking conversation_layer hash..."

EXPECTED=$(grep "conversation_layer.py" .ima/runtime/canonical_online_hash.lock | awk '{print $1}')
CURRENT=$(sha256sum conversation_layer.py | awk '{print $1}')

echo "EXPECTED: $EXPECTED"
echo "CURRENT : $CURRENT"

if [ "$EXPECTED" != "$CURRENT" ]; then
    echo "[FIX] Restoring canonical conversation_layer.py"

    SRC=$(find .ima/backups -name "conversation_layer.py" -exec sha256sum {} \; | grep "$EXPECTED" | head -1 | awk '{print $2}')

    if [ -n "$SRC" ]; then
        cp "$SRC" conversation_layer.py
        echo "[FIX OK] restored from $SRC"
    else
        echo "[FAIL] canonical backup not found"
        exit 1
    fi
else
    echo "[OK] conversation_layer canonical"
fi


echo "[2] Python import tests"

python3 - <<'PY'
import conversation_layer

import ima_master_runtime

import ima_core_runtime
PY


echo "[3] Memory path test"

python3 - <<'PY'
import conversation_layer

c = conversation_layer.context()

conversation_layer.update("IMA canonical verification test")

r = conversation_layer.recall("IMA canonical verification test")

PY


echo "[4] Boot files"

test -f IMA_START.py && echo "[OK] IMA_START"
test -f canonical_boot_guard.py && echo "[OK] boot_guard"
test -f kernel/runtime/CANONICAL/python_bridge.py && echo "[OK] canonical runtime"


echo "[5] Integration audit"

python3 ima_core_integration_audit.py > .ima/runtime/one_shot_audit.json

echo "[OK] audit saved"


echo "=== COMPLETE ==="
