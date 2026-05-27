#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/ima_kernel"

echo "[NORMALIZE] starting full cleanup..."

# kill everything related
pkill -f server.js || true
pkill -f watchdog.sh || true
pkill -f ima_mode.sh || true

# clean bashrc
sed -i '/ima_mode.sh/d' ~/.bashrc

# rebuild single entry point ONLY
cat > $BASE/ima_mode.sh << 'INNER'
#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_kernel

echo "[IMA MODE] booting clean stack..."

# start kernel
nohup node server.js > runtime/logs/server.log 2>&1 &

# start watchdog
nohup bash watchdog.sh > runtime/logs/watchdog.log 2>&1 &

sleep 2

echo "[IMA MODE] health:"
curl -s http://127.0.0.1:3000/health || echo "DOWN"

echo "[IMA MODE] status:"
pgrep -af server.js
pgrep -af watchdog.sh

echo "[IMA MODE] ready"
INNER

chmod +x $BASE/ima_mode.sh

# single boot entry ONLY
mkdir -p ~/.termux/boot

cat > ~/.termux/boot/ima_boot.sh << 'BOOT'
#!/data/data/com.termux/files/usr/bin/bash
bash ~/ima_kernel/ima_mode.sh
BOOT

chmod +x ~/.termux/boot/ima_boot.sh

echo "[DONE] system normalized to single-entry architecture"
