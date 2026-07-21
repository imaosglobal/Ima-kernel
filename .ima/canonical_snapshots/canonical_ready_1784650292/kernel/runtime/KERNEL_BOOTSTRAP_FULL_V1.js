const POOL = require('./KERNEL_EXECUTION_POOL_V1');
const CLUSTER = require('./KERNEL_CLUSTER_MASTER_V8');
const GATEWAY = require('./KERNEL_API_GATEWAY_V3');
const BUS = require('./KERNEL_EVENT_BUS_V2');
const TX = require('./KERNEL_TRANSACTION_ENGINE_V1');

let BOOTED = false;

function start() {
  if (BOOTED || global.__KERNEL_BOOT__) {
    return { status: 'already_booted' };
  }

  global.__KERNEL_BOOT__ = true;
  BOOTED = true;

  // 1. init pool safely
  try {
    if (POOL?.start) POOL.start();
  } catch (e) {
    return { status: 'pool_failed', error: e.message };
  }

  // 2. cluster init (CRITICAL FIX: must pass file if required)
  try {
    if (CLUSTER?.start) {
      CLUSTER.start(__filename); // <-- fixes your previous undefined crash pattern
    }
  } catch (e) {
    return { status: 'cluster_failed', error: e.message };
  }

  return {
    status: 'booted',
    pool: POOL.metrics?.() || null,
    cluster: CLUSTER.metrics?.() || null,
    bus: BUS.all?.()?.length ?? 0
  };
}

function request(cmd) {
  if (!BOOTED) throw new Error('not booted');
  return GATEWAY.request(cmd);
}

function health() {
  return {
    pool: POOL.metrics?.(),
    cluster: CLUSTER.metrics?.(),
    bus: BUS.all?.()?.length ?? 0,
    txSessions: Object.keys(TX.load?.()?.transactions || {}).length
  };
}

function verify() {
  const h = health();

  const issues = [];
  if (!h.pool || h.pool.workers === 0) issues.push('POOL_DOWN');
  if (!h.cluster || h.cluster.workers === 0) issues.push('CLUSTER_DOWN');

  return { ok: issues.length === 0, issues, health: h };
}

module.exports = { start, request, health, verify };
