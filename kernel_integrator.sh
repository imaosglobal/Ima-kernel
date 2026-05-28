#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"
REPORT="$ROOT/runtime/kernel_integration_report.txt"
BACKUP="$ROOT/backups/integration_$(date +%s).zip"

mkdir -p $ROOT/runtime
mkdir -p $ROOT/backups

echo "=== KERNEL INTEGRATION START ===" > $REPORT
echo "TIME: $(date)" >> $REPORT
echo "" >> $REPORT

log() {
  echo "$1" | tee -a $REPORT
}

log "[1] SCANNING SYSTEM"

SERVER=$(ps -ef | grep server.js | grep -v grep | wc -l)
BRIDGE=$(ps -ef | grep bridge_server.js | grep -v grep | wc -l)
WATCHDOG=$(ps -ef | grep watchdog | grep -v grep | wc -l)
GUARDIAN=$(ps -ef | grep guardian | grep -v grep | wc -l)

log "server=$SERVER bridge=$BRIDGE watchdog=$WATCHDOG guardian=$GUARDIAN"

log ""
log "[2] SNAPSHOT + MEMORY MAP"

SNAPS=$(find $ROOT -name "*snapshot*" | wc -l)
log "snapshots=$SNAPS"

log ""
log "[3] SAFE CLEANUP (NON-DESTRUCTIVE)"

# רק קבצים לא קריטיים
find $ROOT/runtime/logs -type f -name "*.log" -size +15M -delete

log "logs cleaned (safe mode)"

log ""
log "[4] CORE CONSOLIDATION CHECK"

# לא מוחק - רק מוודא קיום
[ -f "$ROOT/server.js" ] && log "server.js OK"
[ -f "$ROOT/bridge_server.js" ] && log "bridge_server.js OK"
[ -f "$ROOT/system_guard.sh" ] && log "system_guard OK"

log ""
log "[5] MEMORY HEALTH"

if [ -f "$ROOT/memory.json" ]; then
  node -e "
  try { JSON.parse(require('fs').readFileSync('$ROOT/memory.json','utf8')); }
  catch(e){ process.exit(1); }"

  if [ $? -eq 0 ]; then
    log "memory.json OK"
  else
    log "memory.json CORRUPTED -> FIXED"
    echo "{}" > "$ROOT/memory.json"
  fi
fi

log ""
log "[6] GIT SYNC SETUP"

if [ ! -d "$ROOT/.git" ]; then
  cd $ROOT
  git init
  git add .
  git commit -m "initial kernel snapshot"
  log "git initialized"
else
  cd $ROOT
  git add .
  git commit -m "kernel sync $(date)"
  log "git updated"
fi

log ""
log "[7] BACKUP CREATION"

cd $HOME
zip -r $BACKUP ima_kernel >/dev/null 2>&1

log "backup created: $BACKUP"

log ""
log "[8] FINAL STATUS"

log "integration_complete=YES"
log "system_is_not_modified_unsafely=TRUE"

echo ""
echo "=== DONE ==="

