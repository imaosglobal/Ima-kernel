const POOL = require('./KERNEL_EXECUTION_POOL_V1');
const CLUSTER = require('./KERNEL_CLUSTER_MASTER_V8');
const BUS = require('./KERNEL_EVENT_BUS_V2');

/**
 * SINGLE SOURCE OF TRUTH (minimal safe version)
 */
const STATE = {
  booted: false,
  sessions: new Map(),
  events: []
};

function session(id) {
  if (!STATE.sessions.has(id)) {
    STATE.sessions.set(id, { executed: 0, failed: 0 });
  }
  return STATE.sessions.get(id);
}

function apply(msg, result, ok) {
  if (!msg || !msg.session) return;

  const s = session(msg.session);

  if (ok) s.executed++;
  else s.failed++;

  STATE.events.push({
    session: msg.session,
    node: msg.nodeId,
    ok
  });
}

/**
 * BOOT ONCE
 */
function start() {
  if (STATE.booted) return { status: 'already_booted' };
  STATE.booted = true;

  POOL.start();
  CLUSTER.start();

  // safe hook (only if exists)
  if (typeof CLUSTER.on === 'function') {
    CLUSTER.on('message', (msg) => {
      try {
        const res = POOL.request(msg.cmd);
        apply(msg, res, true);
      } catch (e) {
        apply(msg, { error: e.message }, false);
      }
    });
  }

  return {
    status: 'booted',
    pool: POOL.metrics?.(),
    cluster: CLUSTER.metrics?.()
  };
}

function health() {
  return {
    booted: STATE.booted,
    pool: POOL.metrics?.(),
    cluster: CLUSTER.metrics?.(),
    sessions: STATE.sessions.size,
    events: STATE.events.length,
    ok: (POOL.metrics?.().workers > 0) && (CLUSTER.metrics?.().workers > 0)
  };
}

function verify() {
  const h = health();
  const issues = [];

  if (!h.pool?.workers) issues.push('POOL_DOWN');
  if (!h.cluster?.workers) issues.push('CLUSTER_DOWN');
  if (!h.booted) issues.push('NOT_BOOTED');

  return { ok: issues.length === 0, issues, health: h };
}

module.exports = {
  start,
  health,
  verify
};
