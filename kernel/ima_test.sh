#!/data/data/com.termux/files/usr/bin/bash

echo "=== IMA FULL SYSTEM TEST ==="

echo "[1] restart"
ima restart

sleep 2

echo "[2] health"
ima health

echo "[3] queue"
curl -s http://localhost:4000/v2/queue

echo "[4] logs"
tail -n 30 ~/ima_core/kernel/server.log

echo "=== DONE ==="
