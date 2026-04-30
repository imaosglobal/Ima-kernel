#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

echo "[IMA STATUS]"

HEALTH=$(curl -s http://localhost:4000/health)

echo "Health:"
echo "$HEALTH"

echo ""
echo "Processes:"
ps aux | grep node | grep -v grep

echo ""
echo "State:"
cat ima_state.json
