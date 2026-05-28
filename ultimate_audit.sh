#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"

echo ""
echo "==========================="
echo "IMA ULTIMATE AUDIT"
echo "==========================="
echo ""

mkdir -p $ROOT/runtime/audit
mkdir -p $ROOT/runtime/reports

REPORT="$ROOT/runtime/reports/audit_$(date +%s).log"

touch $REPORT

log() {
  echo "$1" | tee -a $REPORT
}

log ""
log "===== SYSTEM ====="

log "DATE => $(date)"
log "USER => $(whoami)"

log ""
log "===== NODE ====="

node -v 2>&1 | tee -a $REPORT
npm -v 2>&1 | tee -a $REPORT

log ""
log "===== STORAGE ====="

df -h | tee -a $REPORT

log ""
log "===== MEMORY ====="

free -h 2>/dev/null | tee -a $REPORT

log ""
log "===== NODE PROCESSES ====="

ps -ef | grep node | grep -v grep | tee -a $REPORT

log ""
log "===== WATCHDOG ====="

ps -ef | grep watchdog | grep -v grep | tee -a $REPORT

log ""
log "===== LOCK FILES ====="

find $ROOT -name "*.lock" | tee -a $REPORT

log ""
log "===== JSON VALIDATION ====="

find $ROOT -name "*.json" | while read f
do

node -e "
try {
JSON.parse(require('fs').readFileSync('$f','utf8'));
console.log('OK => $f');
} catch(e) {
console.log('BROKEN => $f');
}
" | tee -a $REPORT

done

log ""
log "===== JS SYNTAX ====="

find $ROOT -name "*.js" | while read f
do

node --check "$f" \
>/tmp/ima_check.log 2>&1

if [ $? -eq 0 ]; then
  echo "OK => $f"
else
  echo "BROKEN => $f"
  cat /tmp/ima_check.log
fi

done | tee -a $REPORT

log ""
log "===== DUPLICATE SERVERS ====="

find $ROOT -name "*server*" | tee -a $REPORT

log ""
log "===== TMP FILES ====="

find $ROOT | grep -E "tmp|backup|bak" | tee -a $REPORT

log ""
log "===== PACKAGE CHECK ====="

if [ -f "$ROOT/package.json" ]; then

cd $ROOT

npm audit --omit=dev \
2>&1 | tee -a $REPORT

fi

log ""
log "===== UI CHECK ====="

if [ -d "$ROOT/ima-ui" ]; then

cd $ROOT/ima-ui

if [ -f "package.json" ]; then

npm install \
>> $REPORT 2>&1

npm run build \
>> $REPORT 2>&1

if [ $? -eq 0 ]; then
  echo "UI BUILD OK" | tee -a $REPORT
else
  echo "UI BUILD FAILED" | tee -a $REPORT
fi

fi

fi

log ""
log "===== HEARTBEAT ====="

echo "$(date)" \
> $ROOT/runtime/state/heartbeat.txt

log "HEARTBEAT UPDATED"

log ""
log "===== AUTO SNAPSHOT ====="

STAMP=$(date +%s)

zip -r \
$ROOT/backups/system_snapshot_$STAMP.zip \
$ROOT \
-x "*node_modules*" \
>> $REPORT 2>&1

log "SNAPSHOT => $STAMP"

log ""
log "===== FINAL STATUS ====="

SERVER_COUNT=$(ps -ef | grep node | grep server.js | grep -v grep | wc -l)

WATCHDOG_COUNT=$(ps -ef | grep watchdog.sh | grep -v grep | wc -l)

log "SERVER COUNT => $SERVER_COUNT"
log "WATCHDOG COUNT => $WATCHDOG_COUNT"

if [ "$SERVER_COUNT" -eq 1 ]; then
  log "SERVER STATUS => OK"
else
  log "SERVER STATUS => PROBLEM"
fi

if [ "$WATCHDOG_COUNT" -eq 1 ]; then
  log "WATCHDOG STATUS => OK"
else
  log "WATCHDOG STATUS => PROBLEM"
fi

log ""
log "AUDIT COMPLETE"

echo ""
echo "REPORT:"
echo "$REPORT"
echo ""
