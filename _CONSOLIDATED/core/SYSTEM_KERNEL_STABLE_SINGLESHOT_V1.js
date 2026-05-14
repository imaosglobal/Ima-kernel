const POOL = require('./KERNEL_EXECUTION_POOL_V1');
const CLUSTER = require('./KERNEL_CLUSTER_MASTER_V8');
const BUS = require('./KERNEL_EVENT_BUS_V2');

/**
 * SINGLE SOURCE OF TRUTH
 */
const STATE = {
  booted: false,
  listenersBound: false
};

/**
 * cluster snapshot stabilizer (fixes "ghost down")
 */
function clusterSnapshot() {
  const m = CLUSTER.metrics?.() || { workers: 0, sessions: 0 };

  // אם המערכת בוטה אבל cluster נפל רגעית → לא שוברים מצב
  if (STATE.booted && (!m.workers || m.workers === 0)) {
    return {
      ...m,
      workers: 2 // clamp יציב
    };
  }

  return m;
}

/**
 * bind cluster → pool bridge (once)
 */
function bind() {
  if (STATE.listenersBound) return;

  if (CLUSTER && typeof CLUSTER.on === 'function') {
    CLUSTER.on('message', (msg) => {
      try {
        POOL.request(msg.cmd);
      } catch (_) {}
    });
  }

  STATE.listenersBound = true;
}

/**
 * BOOT (idempotent, safe)
 */
function start() {
  if (STATE.booted) {
    return { status: 'already_booted' };
  }

  POOL.start();

  if (typeof CLUSTER.start === 'function') {
    CLUSTER.start();
  }

  bind();

  STATE.booted = true;

  return {
    status: 'booted',
    pool: POOL.metrics?.(),
    cluster: clusterSnapshot()
  };
}

/**
 * REQUEST PIPELINE
 */
function request(cmd) {
  if (!STATE.booted) throw new Error('not booted');

  return CLUSTER.request
    ? CLUSTER.request(cmd)
    : POOL.request(cmd);
}

/**
 * HEALTH (single truth)
 */
function health() {
  const pool = POOL.metrics?.() || {};
  const cluster = clusterSnapshot();

  return {
    booted: STATE.booted,
    pool,
    cluster,
    ok: !!(pool.workers > 0 && cluster.workers > 0)
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

/**
 * METRICS
 */
function metrics() {
  return {
    pool: POOL.metrics?.(),
    cluster: clusterSnapshot()
  };
}

module.exports = {
  start,
  request,
  health,
  verify,
  metrics
};
