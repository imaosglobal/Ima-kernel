#!/data/data/com.termux/files/usr/bin/bash

set -e

BASE="$HOME/ima_kernel"

echo "[IMA FIX] cleaning duplicates..."

# 1. remove duplicates from bashrc
sed -i '/ima_mode.sh/d' ~/.bashrc
sed -i '/server.js/d' ~/.bashrc
sed -i '/ima_kernel/d' ~/.bashrc

# 2. ensure directories exist
mkdir -p $BASE/runtime/logs

# 3. stop old processes
pkill -f server.js || true
pkill -f watchdog.sh || true

# 4. start kernel clean
nohup node $BASE/server.js > $BASE/runtime/logs/server.log 2>&1 &
nohup bash $BASE/watchdog.sh > $BASE/runtime/logs/watchdog.log 2>&1 &

# 5. create single entry mode loader
cat > $BASE/ima_mode.sh << 'INNER'
#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_kernel

echo "[IMA MODE] starting..."

# health check
curl -s http://127.0.0.1:3000/health || echo "[WARN] kernel not responding"

echo "[IMA MODE] kernel directory:"
pwd

echo "[IMA MODE] logs:"
ls -lt runtime/logs | head

echo "[IMA MODE] ready"
INNER

chmod +x $BASE/ima_mode.sh

# 6. clean boot entry (ONLY ONE)
mkdir -p ~/.termux/boot

cat > ~/.termux/boot/ima_boot.sh << 'BOOT'
#!/data/data/com.termux/files/usr/bin/bash
cd ~/ima_kernel
bash ima_mode.sh
BOOT

chmod +x ~/.termux/boot/ima_boot.sh

echo "[DONE] IMA system normalized"
echo "Only entry: ima_mode.sh + termux-boot"
