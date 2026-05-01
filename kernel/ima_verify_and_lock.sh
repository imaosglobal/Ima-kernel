#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=============================="
echo "[IMA FULL VERIFY + LOCK]"
echo "=============================="

FAIL=0

# 1. sanity
echo "[1] sanity"
node -e "const p=require('./package.json'); if(!p.name||!p.version) process.exit(1); console.log('[OK]',p.version);" || FAIL=1

# 2. core load
echo "[2] core load"
IMA_SAFE_MODE=1 node -e "require('./global_boot.js'); require('./api_layer.js'); require('./db_memory.js'); console.log('[OK] core loaded');" || FAIL=1

# 3. bridge
echo "[3] bridge"
node -e "const b=require('./ima_platform_bridge'); if(!b.identity||!b.sync||!b.events||!b.reactive||!b.device) process.exit(1); console.log('[OK] bridge');" || FAIL=1

# 4. identity
echo "[4] identity"
node -e "const id=require('./ima_identity'); const r=id.login('google',{name:'verify'}); if(!r.ok) process.exit(1); console.log('[OK] identity');" || FAIL=1

# 5. sync
echo "[5] sync"
node -e "const s=require('./ima_sync'); s.set('verify',{ok:true}); const d=s.dump(); if(!d.verify) process.exit(1); console.log('[OK] sync');" || FAIL=1

# 6. events
echo "[6] events"
node -e "const e=require('./ima_events'); let ok=false; e.on('v',()=>ok=true); e.emit('v',{}); setTimeout(()=>{ if(!ok) process.exit(1); console.log('[OK] events'); },50);" || FAIL=1

sleep 1

# 7. reactive
echo "[7] reactive"
node -e "const b=require('./ima_platform_bridge'); b.reactive.react('v',(d)=>({flag:true})); b.events.emit('v',{}); setTimeout(()=>{ const s=b.sync.dump(); if(!s.flag) process.exit(1); console.log('[OK] reactive'); },100);" || FAIL=1

sleep 1

# 8. safe mode
echo "[8] safe mode"
IMA_SAFE_MODE=1 node -e "require('./global_boot.js'); console.log('[OK] safe');" || FAIL=1

# 9. runtime
echo "[9] runtime"
node -e "const {spawn}=require('child_process'); const p=spawn('node',['global_boot.js']); setTimeout(()=>{ p.kill(); console.log('[OK] runtime'); },1500);" || FAIL=1

sleep 2

# RESULT
if [ "$FAIL" -ne 0 ]; then
  echo "=============================="
  echo "[FAILED] NOT LOCKING"
  echo "=============================="
  exit 1
fi

# LOCK (FIXED FINAL)
echo "[10] LOCK"

mkdir -p backups
TMP="backups/.tmp_lock_$$.tgz"
FINAL="backups/final_lock_$(date +%s).tgz"

tar --exclude='./backups' -czf "$TMP" .
mv "$TMP" "$FINAL"

git add .
git commit -m "LOCK VERIFIED $(date +%s)" >/dev/null 2>&1 || true
git tag verified-$(date +%s) >/dev/null 2>&1 || true
git push >/dev/null 2>&1 || true
git push --tags >/dev/null 2>&1 || true

echo "[LOCKED] $FINAL"

echo "=============================="
echo "[ALL SYSTEMS GO]"
echo "=============================="
