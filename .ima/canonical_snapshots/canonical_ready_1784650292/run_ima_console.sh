#!/data/data/com.termux/files/usr/bin/bash

echo "=== IMA SYSTEM START ==="

cd ~/ima_kernel

# בדיקת API קיים
if curl -s http://127.0.0.1:8080/health | grep -q '"health": "ok"'; then
    echo "[OK] API already running"
else
    echo "[START] API"
    pkill -f "api/server.py" 2>/dev/null || true
    python3 api/server.py &
    sleep 2
fi

# בדיקת UI
cd ~/ima_kernel/ima-ui

if [ ! -d "node_modules" ]; then
    echo "[INSTALL] UI dependencies"
    npm install
fi

echo "[BUILD] IMA Console"
npm run build

echo "[START] IMA Console"

npm run dev -- --host 0.0.0.0
