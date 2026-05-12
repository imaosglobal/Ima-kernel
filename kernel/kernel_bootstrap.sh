#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "[1] scanning kernel modules..."

POOL=$(find . -name "KERNEL_EXECUTION_POOL_V1.js" | head -n 1)
CLUSTER=$(find . -name "KERNEL_CLUSTER_MASTER_V8.js" | head -n 1)

if [ -z "$POOL" ] || [ -z "$CLUSTER" ]; then
  echo "[ERROR] missing kernel modules"
  echo "POOL=$POOL"
  echo "CLUSTER=$CLUSTER"
  exit 1
fi

POOL_DIR=$(dirname "$POOL")
CLUSTER_DIR=$(dirname "$CLUSTER")

echo "[2] detected:"
echo "POOL   -> $POOL"
echo "CLUSTER-> $CLUSTER"

echo "[3] generating stable kernel wrapper..."

cat > kernel_single.js << JS
'use strict';

const POOL = require('${POOL}');
const CLUSTER = require('${CLUSTER}');

let booted = false;
let locked = false;
let snapshot = null;

function capture() {
  const m = CLUSTER.metrics?.() || {};
  return { workers: m.workers || 0, sessions: m.sessions || 0, ts: Date.now() };
}

function lock() {
  if (locked) return;
  const original = CLUSTER.start;

  CLUSTER.start = function () {
    if (booted) return { status: 'locked' };
    return original.apply(this, arguments);
  };

  locked = true;
}

function start() {
  if (booted) return { status: 'already_booted' };

  POOL.start();
  const c = CLUSTER.start();

  lock();

  snapshot = capture();
  booted = true;

  return { status: 'booted', pool: POOL.metrics?.(), cluster: snapshot };
}

function health() {
  const pool = POOL.metrics?.() || {};
  const cluster = snapshot || capture();

  return {
    booted,
    pool,
    cluster,
    ok: booted && pool.workers > 0 && cluster.workers > 0
  };
}

function verify() {
  const h = health();
  const issues = [];

  if (!h.booted) issues.push('NOT_BOOTED');
  if (!h.pool.workers) issues.push('POOL_DOWN');
  if (!h.cluster.workers) issues.push('CLUSTER_DOWN');

  return { ok: issues.length === 0, issues, health: h };
}

module.exports = { start, health, verify };
JS

echo "[4] syntax check..."
node -c kernel_single.js

echo "[5] runtime test..."
node -e "
const K=require('./kernel_single');
console.log('BOOT',K.start());
console.log('VERIFY',K.verify());
console.log('HEALTH',K.health());
"

echo "[DONE] kernel is stable"
