#!/data/data/com.termux/files/usr/bin/bash

set -e

BASE=~/ima_kernel

echo "[NORMALIZE] stopping runtime processes..."
pkill -f server.js || true
pkill -f watchdog.sh || true

echo "[NORMALIZE] cleaning git noise..."

cd $BASE

# keep only kernel + core + cloud + runtime + main entry scripts
git add -A

echo "[NORMALIZE] building snapshot state..."

mkdir -p kernel/cloud

node -e "
const fs=require('fs');

const base=process.env.HOME+'/ima_kernel/kernel/cloud';

const memPath=base+'/memory.json';

let mem={memory:[]};

try {
  mem=JSON.parse(fs.readFileSync(memPath,'utf8'));
} catch(e){}

const state={
  timestamp:Date.now(),
  total_entries:(mem.memory||[]).length,
  status:'normalized'
};

fs.writeFileSync(base+'/state.json',JSON.stringify(state,null,2));

console.log('[OK] state normalized');
"

echo "[NORMALIZE] committing clean snapshot..."

git commit -m "IMA SYSTEM NORMALIZATION $(date)" || echo "no changes to commit"

echo "[NORMALIZE] pushing to origin..."

git push origin main || echo "push failed (check auth)"

echo "[NORMALIZE] restarting system..."

nohup node ~/ima_kernel/server.js > ~/ima_kernel/runtime/logs/server.log 2>&1 &
nohup bash ~/ima_kernel/watchdog.sh > ~/ima_kernel/runtime/logs/watchdog.log 2>&1 &

echo "[DONE] system normalized + running"
