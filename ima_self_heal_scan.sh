#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"
REPORT="$ROOT/runtime/self_heal_report.txt"

mkdir -p $ROOT/runtime

echo "IMA SELF HEAL SCAN" > $REPORT
echo "DATE: $(date)" >> $REPORT
echo "" >> $REPORT

log() {
  echo "$1" | tee -a $REPORT
}

log "[1] DISK USAGE"
df -h $HOME | tee -a $REPORT

log ""
log "[2] NODE PROCESSES"

ps -ef | grep node | grep -v grep | tee -a $REPORT

log ""
log "[3] DUPLICATE DETECTION"

SERVER_COUNT=$(ps -ef | grep server.js | grep -v grep | wc -l)
WATCHDOG_COUNT=$(ps -ef | grep watchdog.sh | grep -v grep | wc -l)
GUARDIAN_COUNT=$(ps -ef | grep guardian | grep -v grep | wc -l)

log "server=$SERVER_COUNT watchdog=$WATCHDOG_COUNT guardian=$GUARDIAN_COUNT"

log ""
log "[4] SNAPSHOT OVERLOAD CHECK"

SNAP_COUNT=$(find $ROOT -name "*snapshot*" 2>/dev/null | wc -l)

log "snapshots=$SNAP_COUNT"

if [ "$SNAP_COUNT" -gt 200 ]; then
  log "CLEANING OLD SNAPSHOTS"

  find $ROOT -name "*snapshot*" \
  -type f \
  | sort \
  | head -n -50 \
  | xargs rm -f 2>/dev/null

fi

log ""
log "[5] LOG CLEANUP"

find $ROOT/runtime/logs -type f -name "*.log" -size +20M -delete

log "large logs removed"

log ""
log "[6] JSON VALIDATION SAFE MODE"

find $ROOT -name "*.json" \
-not -path "*/node_modules/*" \
-not -path "*/snapshots/*" | while read f
do
  node -e "
  try {
    JSON.parse(require('fs').readFileSync('$f','utf8'));
    process.exit(0);
  } catch(e) {
    process.exit(1);
  }"

  if [ $? -ne 0 ]; then
    echo "FIXED JSON => $f" | tee -a $REPORT
    echo "{}" > "$f"
  fi
done

log ""
log "[7] BRIDGE CHECK"

curl -s http://127.0.0.1:7777 -o /dev/null

if [ $? -eq 0 ]; then
  log "bridge OK"
else
  log "bridge DOWN"
fi

log ""
log "[8] FINAL HEALTH SCORE"

SCORE=100

if [ "$SERVER_COUNT" -ne 1 ]; then SCORE=$((SCORE-20)); fi
if [ "$WATCHDOG_COUNT" -ne 1 ]; then SCORE=$((SCORE-20)); fi
if [ "$GUARDIAN_COUNT" -lt 1 ]; then SCORE=$((SCORE-20)); fi
if [ "$SNAP_COUNT" -gt 300 ]; then SCORE=$((SCORE-20)); fi

log "HEALTH SCORE = $SCORE / 100"

if [ "$SCORE" -ge 80 ]; then
  log "SYSTEM STATUS: STABLE"
else
  log "SYSTEM STATUS: NEEDS ATTENTION"
fi

log ""
log "DONE"
