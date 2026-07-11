#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"
ENTRY="IMA_START.py"

echo "=== IMA DEVELOPMENT GATE ==="

cd "$ROOT" || exit 1

echo "[1] Checking canonical entry"

if [ ! -f "$ENTRY" ]; then
    echo "ERROR: Missing canonical entry"
    exit 1
fi

echo "[2] Running IMA validation"

python3 "$ENTRY"

if [ $? -ne 0 ]; then
    echo "BLOCKED: IMA validation failed"
    exit 1
fi

echo "[3] Development approved"
echo "All changes must pass through:"
echo "$ENTRY"

exit 0
