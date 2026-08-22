#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA PRODUCT CONNECTION AUDIT ==="

echo
echo "[API]"
find api -maxdepth 2 -type f | sort

echo
echo "[FRONTEND]"
find frontend -maxdepth 2 -type f | sort

echo
echo "[ANDROID]"
find android/app/src -maxdepth 4 -type f 2>/dev/null | sort

echo
echo "[PRODUCT]"
find product -maxdepth 3 -type f | sort

echo
echo "[AUTH]"
find auth -maxdepth 3 -type f | sort

echo
echo "[DATABASE]"
find database -maxdepth 3 -type f | sort

echo
echo "[IMPORT CHECK]"
python3 - <<'PY'
mods=[
"ima_master_runtime",
"ima_core_runtime",
"conversation_layer",
"api.server"
]

for m in mods:
    try:
        __import__(m)
    except Exception as e:
PY

echo
echo "=== COMPLETE ==="
