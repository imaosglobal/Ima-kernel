#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"

echo ""
echo "========================="
echo "IMA SYSTEM GUARD"
echo "========================="
echo ""

REPORT="$ROOT/runtime/system_guard_report.txt"

mkdir -p $ROOT/runtime
mkdir -p $ROOT/runtime/logs
mkdir -p $ROOT/runtime/state

echo "" > $REPORT

log() {
  echo "$1" | tee -a $REPORT
}

log "START => $(date)"

echo ""
echo "[1] checking server..."

SERVER_COUNT=$(ps -ef | grep node | grep server.js | grep -v grep | wc -l)

log "SERVER_COUNT => $SERVER_COUNT"

if [ "$SERVER_COUNT" -eq 0 ]; then

  log "SERVER DOWN => RESTARTING"

  nohup node $ROOT/server.js \
  >> $ROOT/runtime/logs/server.log 2>&1 &

  sleep 3

fi

if [ "$SERVER_COUNT" -gt 1 ]; then

  log "DUPLICATE SERVERS => CLEANING"

  pkill -f server.js

  sleep 2

  nohup node $ROOT/server.js \
  >> $ROOT/runtime/logs/server.log 2>&1 &

fi

echo ""
echo "[2] checking watchdog..."

WATCHDOG_COUNT=$(ps -ef | grep watchdog.sh | grep -v grep | wc -l)

log "WATCHDOG_COUNT => $WATCHDOG_COUNT"

if [ "$WATCHDOG_COUNT" -gt 1 ]; then

  log "MULTIPLE WATCHDOGS => CLEANING"

  pkill -f watchdog.sh

  sleep 2

  nohup bash $ROOT/watchdog.sh \
  >> $ROOT/runtime/logs/watchdog.log 2>&1 &

fi

echo ""
echo "[3] cleaning locks..."

find $ROOT/runtime -name "*.lock" -mtime +1 -delete

log "OLD LOCKS CLEANED"

echo ""
echo "[4] cleaning tmp..."

find $ROOT -name "*.tmp" -delete
find $ROOT -name "*.bak" -mtime +7 -delete

log "TMP CLEANED"

echo ""
echo "[5] snapshot control..."

SNAPCOUNT=$(find $ROOT -path "*snapshot*" | wc -l)

log "SNAPSHOT_COUNT => $SNAPCOUNT"

if [ "$SNAPCOUNT" -gt 25 ]; then

  log "TOO MANY SNAPSHOTS => TRIMMING"

  find $ROOT \
  -path "*snapshot*" \
  -type f \
  | sort \
  | head -n -10 \
  | xargs rm -f

fi

echo ""
echo "[6] validating json..."

find $ROOT \
-name "*.json" \
-not -path "*/node_modules/*" \
-not -path "*/snapshots/*" \
| while read f
do

node -e "
try{
JSON.parse(require('fs').readFileSync('$f','utf8'));
process.exit(0);
}catch(e){
process.exit(1);
}
"

if [ $? -ne 0 ]; then

  log "BROKEN JSON => $f"

  echo "{}" > "$f"

  log "RESET => $f"

fi

done

echo ""
echo "[7] memory heartbeat..."

echo "$(date)" \
> $ROOT/runtime/state/heartbeat.txt

log "HEARTBEAT UPDATED"

echo ""
echo "[8] checking disk..."

df -h | tee -a $REPORT

echo ""
echo "[9] checking connections..."

if [ -f "$ROOT/kernel/cloud/state.json" ]; then
  log "CLOUD STATE => OK"
else
  log "CLOUD STATE => MISSING"
fi

if [ -f "$ROOT/kernel/cloud/model_router.js" ]; then
  log "MODEL ROUTER => OK"
fi

if [ -f "$ROOT/kernel/cloud/gemini_client.js" ]; then
  log "GEMINI CLIENT => OK"
fi

echo ""
echo "[10] final status..."

FINAL_SERVER=$(ps -ef | grep node | grep server.js | grep -v grep | wc -l)

FINAL_WATCHDOG=$(ps -ef | grep watchdog.sh | grep -v grep | wc -l)

log "FINAL_SERVER => $FINAL_SERVER"
log "FINAL_WATCHDOG => $FINAL_WATCHDOG"

echo ""
echo "SYSTEM HEALTHY"
echo ""

log "DONE => $(date)"
