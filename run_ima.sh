#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_kernel

pkill -f "node ima.js"

sleep 1

nohup node ima.js > logs/runtime.log 2>&1 &

sleep 3

curl -s localhost:7000/health

echo
echo "[IMA OS BOOTED]"
