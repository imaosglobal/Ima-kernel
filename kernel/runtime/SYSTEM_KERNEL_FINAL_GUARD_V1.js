const POOL = require('./KERNEL_EXECUTION_POOL_V1');
const CLUSTER = require('./KERNEL_CLUSTER_MASTER_V8');

const STATE = {
  booted: false
};

let POOL_LOCK = false;
let CLUSTER_LOCK = false;

/**
 * POOL SAFE WRAP
 */
const safePoolStart = (() => {
  const original = POOL.start;

  return function () {
    if (POOL_LOCK) return { status: 'pool_already_started' };
    POOL_LOCK = true;
    return original.apply(this, arguments);
  };
})();

/**
 * CLUSTER SAFE WRAP
 */
const safeClusterStart = (() => {
  const original = CLUSTER.start;

  return function () {
    if (CLUSTER_LOCK) return { status: 'cluster_already_started' };
    CLUSTER_LOCK = true;
    return original.apply(this, arguments);
  };
})();

/**
 * BOOT
 */
function start() {
  if (STATE.booted) {
    return { status: 'already_booted' };
  }

  STATE.booted = true;

  safePoolStart();
  safeClusterStart();

  return {
    status: 'booted',
    pool: POOL.metrics?.(),
    cluster: CLUSTER.metrics?.()
  };
}

/**
 * HEALTH
 */
function health() {
  return {
    booted: STATE.booted,
    pool: POOL.metrics?.(),
    cluster: CLUSTER.metrics?.(),
    ok: (POOL.metrics?.().workers > 0) && (CLUSTER.metrics?.().workers > 0)
  };
}

/**
 * VERIFY
 */
function verify() {
  const h = health();
  const issues = [];

  if (!h.pool.workers) issues.push('POOL_DOWN');
  if (!h.cluster.workers) issues.push('CLUSTER_DOWN');
  if (!h.booted) issues.push('NOT_BOOTED');

  return {
    ok: issues.length === 0,
    issues,
    health: h
  };
}

module.exports = {
  start,
  health,
  verify
};
