#!/data/data/com.termux/files/usr/bin/bash

echo "[IMA REPAIR] restarting runtime safely..."

pkill -f prod_server.js || true
pkill -f node || true

sleep 2

bash ~/ima_core/kernel/ima_update.sh

echo "[IMA REPAIR] done"
