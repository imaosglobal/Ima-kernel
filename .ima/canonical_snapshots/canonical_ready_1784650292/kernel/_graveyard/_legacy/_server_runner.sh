#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

echo $$ > server.pid

echo "[IMA FIXED RUNNER] starting clean node..."

# FORCE CLEAN EXECUTION (no wrapper)
exec env -i PATH=/data/data/com.termux/files/usr/bin:/usr/bin:/bin \
  /data/data/com.termux/files/usr/bin/node ./prod_server.js
