#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

echo "=== IMA KERNEL STABLE MANAGER ==="

# =========================
# 1. SOURCE OF TRUTH
# =========================
mkdir -p kernel_state backups logs releases

DATE=$(date +%F)
TIME=$(date +%T)

# =========================
# 2. SYSTEM SNAPSHOT
# =========================
echo "[1] Creating snapshot..."

cp ima_db.json backups/db_$DATE.json 2>/dev/null
cp ima_pro_saas.js backups/server_$DATE.js 2>/dev/null

git add . >/dev/null 2>&1
git commit -m "auto snapshot $DATE $TIME" >/dev/null 2>&1
git push origin main >/dev/null 2>&1

# =========================
# 3. VERSION CONTROL
# =========================
if [ ! -f VERSION ]; then
  echo "1.0.0" > VERSION
fi

VERSION=$(cat VERSION)
echo "[2] Current VERSION: $VERSION"

# =========================
# 4. HEALTH CHECK
# =========================
echo "[3] Health check..."

if ! curl -s http://localhost:4000/run \
  -H "x-api-key: $(cat ~/.ima_key 2>/dev/null)" \
  -H "Content-Type: application/json" \
  --data-raw '{"task":"kernel_check"}' | grep -q ok; then

  echo "⚠ SYSTEM UNHEALTHY → restarting"
  pkill -f ima_pro_saas.js || true
  node ~/ima_core/kernel/ima_pro_saas.js &
else
  echo "✔ SYSTEM OK"
fi

# =========================
# 5. USAGE LOGGING
# =========================
echo "{\"time\":\"$TIME\",\"status\":\"ok\",\"version\":\"$VERSION\"}" >> logs/daily.log

# =========================
# 6. AUTO BOOT GUARD
# =========================
pgrep -f ima_pro_saas.js >/dev/null || node ~/ima_core/kernel/ima_pro_saas.js &

echo "=== KERNEL COMPLETE ==="
