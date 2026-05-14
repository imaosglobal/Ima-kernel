const POOL = require('./KERNEL_EXECUTION_POOL_V1');
const CLUSTER = require('./KERNEL_CLUSTER_MASTER_V8');
const BUS = require('./KERNEL_EVENT_BUS_V2');
const LOG = require('./SYSTEM_EVENT_LOG_RUNTIME_V1');

let BOOTED = false;

// --------------------
// BOOT
// --------------------
function start() {
  if (BOOTED) return { status: 'already_booted' };
  BOOTED = true;

  POOL.start?.();
  CLUSTER.start?.();

  return {
    status: 'booted',
    pool: POOL.metrics?.(),
    cluster: CLUSTER.metrics?.()
  };
}

// --------------------
// SAFE REQUEST PIPELINE
// --------------------
function request(cmd) {
  if (!BOOTED) throw new Error('kernel not booted');

  const logEntry = LOG.logRequest(cmd);

  const res = POOL.request(cmd);

  LOG.logResult(logEntry.ts, res, 'done');

  return res;
}

// --------------------
// REPLAY FROM LOG
// --------------------
function replay() {
  return LOG.replay((cmd) => {
    return POOL.request(cmd);
  });
}

// --------------------
// HEALTH
// --------------------
function health() {
  return {
    pool: POOL.metrics?.(),
    cluster: CLUSTER.metrics?.(),
    bus: BUS.all?.()?.length ?? 0,
    log: LOG.snapshot?.()
  };
}

// --------------------
// VERIFY CONSISTENCY
// --------------------
function verify() {
  const h = health();

  const issues = [];

  if (!h.pool || h.pool.workers === 0) issues.push('POOL_DOWN');
  if (!h.cluster || h.cluster.workers === 0) issues.push('CLUSTER_DOWN');

  return {
    ok: issues.length === 0,
    issues,
    health: h
  };
}

module.exports = {
  start,
  request,
  replay,
  health,
  verify
};

// auto boot test
if (require.main === module) {
  console.log('[BOOT]', start());

  const r1 = request({
    type: 'WRITE_FILE',
    file: './runtime/unified_test.js',
    content: 'console.log("UNIFIED OK")'
  });

  setTimeout(() => {
    console.log('[HEALTH]', health());
    console.log('[VERIFY]', verify());
    console.log('[REPLAY]', replay());
  }, 1500);
}
