#!/data/data/com.termux/files/usr/bin/bash

echo "=== IMA DOCTOR ==="

echo "[1] health"
ima health

echo ""
echo "[2] queue"
ima queue

echo ""
echo "[3] routes check"
grep -n "app.use(\"/v2" ~/ima_core/kernel/prod_server.js

echo ""
echo "[4] duplicate detection"
grep -n "taskRoutes\|productRoutes" ~/ima_core/kernel/prod_server.js

echo ""
echo "[5] node status"
ps aux | grep node | grep -v grep

echo ""
echo "=== DONE ==="
