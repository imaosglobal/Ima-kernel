const fs = require('fs');
const path = require('path');

const POOL = require('./KERNEL_EXECUTION_POOL_V1');
const CLUSTER = require('./KERNEL_CLUSTER_MASTER_V8');
const LOG = require('./SYSTEM_EVENT_LOG_RUNTIME_V1');

let STATE = {
  booted: false,
  replayed: false,
  snapshot: null
};

// ------------------------
// LOAD EVENT LOG
// ------------------------
function loadLog() {
  return LOG.replay((cmd) => {
    return POOL.request(cmd);
  });
}

// ------------------------
// REBUILD SYSTEM STATE
// ------------------------
function rebuild() {
  const replay = loadLog();

  STATE.snapshot = {
    executed: replay.executed,
    failed: replay.failed,
    results: replay.results.length
  };

  return STATE.snapshot;
}

// ------------------------
// REHYDRATE SYSTEM (CORE)
// ------------------------
function start() {
  if (STATE.booted) return STATE;

  STATE.booted = true;

  // IMPORTANT:
  // NO cluster.start() here intentionally
  // system is reconstructed from log

  POOL.start?.();

  const snapshot = rebuild();

  STATE.replayed = true;

  return {
    status: 'rehydrated',
    snapshot,
    pool: POOL.metrics?.()
  };
}

// ------------------------
// LIVE REQUEST (still allowed)
// ------------------------
function request(cmd) {
  if (!STATE.booted) throw new Error('not rehydrated');

  return POOL.request(cmd);
}

// ------------------------
// HEALTH
// ------------------------
function health() {
  return {
    pool: POOL.metrics?.(),
    cluster: CLUSTER.metrics?.(), // passive read only
    snapshot: STATE.snapshot,
    booted: STATE.booted
  };
}

// ------------------------
// VERIFY CONSISTENCY
// ------------------------
function verify() {
  const h = health();

  const issues = [];

  if (!h.pool || h.pool.workers === 0) issues.push('POOL_DOWN');

  return {
    ok: issues.length === 0,
    issues,
    health: h
  };
}

// ------------------------
module.exports = {
  start,
  request,
  health,
  verify,
  rebuild
};

// self test
if (require.main === module) {
  console.log('[REHYDRATE]', start());

  const r = request({
    type: 'WRITE_FILE',
    file: './runtime/rehydrated_test.js',
    content: 'console.log("REHYDRATED OK")'
  });

  setTimeout(() => {
    console.log('[HEALTH]', health());
    console.log('[VERIFY]', verify());
  }, 1200);
}
