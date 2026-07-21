const fs = require('fs');
const path = require('path');
const cluster = require('cluster');

const POOL = require('./KERNEL_EXECUTION_POOL_V1');
const BUS = require('./KERNEL_EVENT_BUS_V2');

let BOOTED = false;

// -----------------------------
// SAFE CLUSTER BOOT (ROOT FIX)
// -----------------------------
function startCluster(workers = 2) {

  if (!cluster.isPrimary) {
    return { status: 'not_primary' };
  }

  if (BOOTED) {
    return { status: 'already_booted' };
  }

  BOOTED = true;

  const workerPath = path.join(__dirname, 'KERNEL_CLUSTER_WORKER_BOOT.js');

  if (!fs.existsSync(workerPath)) {
    throw new Error('[FATAL] missing worker boot file: ' + workerPath);
  }

  console.log('[CLUSTER] starting with workers:', workers);

  cluster.setupPrimary({
    exec: workerPath
  });

  for (let i = 0; i < workers; i++) {
    const w = cluster.fork({ WORKER_ID: String(i) });

    // חשוב: לראות מוות אמיתי
    w.on('exit', (code, signal) => {
      console.log('[CLUSTER EXIT]', {
        worker: w.process?.pid,
        code,
        signal
      });
    });

    w.on('error', (err) => {
      console.log('[CLUSTER ERROR]', err.message);
    });
  }

  cluster.on('online', (w) => {
    console.log('[CLUSTER ONLINE]', w.process?.pid);
  });

  return { status: 'started', workers };
}

// -----------------------------
// HEALTH CHECK (REAL STATE)
// -----------------------------
function metrics() {
  return {
    pool: POOL.metrics?.(),
    cluster: {
      workers: Object.keys(cluster.workers || {}).length
    },
    bus: BUS.all?.()?.length ?? 0,
    booted: BOOTED
  };
}

// -----------------------------
// VERIFY CONSISTENCY
// -----------------------------
function verify() {
  const m = metrics();

  const issues = [];

  if (!m.pool || m.pool.workers === 0) {
    issues.push('POOL_DOWN');
  }

  if (!m.cluster || m.cluster.workers === 0) {
    issues.push('CLUSTER_DOWN');
  }

  return {
    ok: issues.length === 0,
    issues,
    snapshot: m
  };
}

// -----------------------------
// FULL SELF TEST
// -----------------------------
function runSelfTest() {

  console.log('[SELF TEST] booting system...');

  try {
    POOL.start?.();
  } catch (e) {
    console.log('[POOL ERROR]', e.message);
  }

  startCluster(2);

  setTimeout(() => {

    const m1 = metrics();

    console.log('[METRICS 2s]', m1);

    setTimeout(() => {

      const m2 = metrics();
      const v = verify();

      console.log('[METRICS 4s]', m2);
      console.log('[VERIFY]', v);

    }, 2000);

  }, 2000);
}

module.exports = {
  startCluster,
  metrics,
  verify,
  runSelfTest
};

// auto-run mode
if (require.main === module) {
  runSelfTest();
}
