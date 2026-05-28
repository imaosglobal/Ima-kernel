#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"
LOG="$ROOT/runtime/logs/control_center.log"
REPORT="$ROOT/runtime/control_report.txt"

mkdir -p $ROOT/runtime/logs

echo "=== CONTROL CENTER RUN ===" > $REPORT
echo "TIME: $(date)" >> $REPORT
echo "" >> $REPORT

log() {
  echo "$1" | tee -a $REPORT
}

log "[1] PROCESS CHECK"

SERVER=$(ps -ef | grep server.js | grep -v grep | wc -l)
WATCHDOG=$(ps -ef | grep watchdog.sh | grep -v grep | wc -l)
GUARDIAN=$(ps -ef | grep guardian | grep -v grep | wc -l)
BRIDGE=$(ps -ef | grep bridge_server.js | grep -v grep | wc -l)

log "server=$SERVER watchdog=$WATCHDOG guardian=$GUARDIAN bridge=$BRIDGE"

log ""
log "[2] DISK CHECK"

DISK=$(df $HOME | tail -1 | awk '{print $5}' | sed 's/%//')
log "disk_usage=$DISK%"

if [ "$DISK" -gt 90 ]; then
  log "DISK ALERT -> CLEANING LOGS"

  find $ROOT/runtime/logs -type f -name "*.log" -size +10M -delete
fi

log ""
log "[3] SNAPSHOT CONTROL"

SNAPS=$(find $ROOT -name "*snapshot*" 2>/dev/null | wc -l)
log "snapshots=$SNAPS"

if [ "$SNAPS" -gt 200 ]; then
  log "SNAPSHOT OVERLOAD -> TRIMMING"

  BEFORE=$(find $ROOT -name "*snapshot*" | wc -l)

  find $ROOT -name "*snapshot*" \
  -type f | sort | head -n -50 | xargs rm -f

  AFTER=$(find $ROOT -name "*snapshot*" | wc -l)

  log "snapshots_before=$BEFORE snapshots_after=$AFTER"
fi

log ""
log "[4] BRIDGE CHECK"

curl -s http://127.0.0.1:7777 -o /dev/null

if [ $? -eq 0 ]; then
  log "bridge_status=OK"
else
  log "bridge_status=DOWN -> restart needed"
fi

log ""
log "[5] SELF HEAL (SAFE MODE)"

# רק אם משהו שבור ממש
if [ "$SERVER" -eq 0 ]; then
  log "server_restart"
  nohup node $ROOT/server.js >> $ROOT/runtime/logs/server.log 2>&1 &
fi

if [ "$BRIDGE" -eq 0 ]; then
  log "bridge_restart"
  nohup node $ROOT/bridge_server.js >> $ROOT/runtime/logs/bridge.log 2>&1 &
fi

log ""
log "[6] FINAL VERIFICATION"

sleep 2

SERVER2=$(ps -ef | grep server.js | grep -v grep | wc -l)
BRIDGE2=$(ps -ef | grep bridge_server.js | grep -v grep | wc -l)

log "server_after=$SERVER2 bridge_after=$BRIDGE2"

log ""
log "STATUS: DONE"

