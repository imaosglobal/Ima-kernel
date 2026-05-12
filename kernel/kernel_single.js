'use strict';

const POOL = require('./KERNEL_EXECUTION_POOL_V1');
const CLUSTER = require('./KERNEL_CLUSTER_MASTER_V8');

const STATE = {
  booted: false,
  clusterLocked: false,
  snapshot: null
};

function captureClusterState() {
  const m = CLUSTER.metrics?.() || {};
  return {
    workers: m.workers || 0,
    sessions: m.sessions || 0,
    ts: Date.now()
  };
}

let clusterStarted = false;
let lockApplied = false;

function startClusterSafe() {
  if (clusterStarted) return { status: 'already_started' };
  clusterStarted = true;
  return CLUSTER.start();
}

function lockCluster() {
  if (lockApplied) return;

  const original = CLUSTER.start;

  CLUSTER.start = function () {
    if (STATE.booted) {
      return { status: 'cluster_locked' };
    }
    return original.apply(this, arguments);
  };

  lockApplied = true;
}

function start() {
  if (STATE.booted) return { status: 'already_booted' };

  POOL.start();
  const cluster = startClusterSafe();

  lockCluster();

  STATE.snapshot = captureClusterState();
  STATE.booted = true;

  return {
    status: 'booted',
    pool: POOL.metrics?.(),
    cluster: STATE.snapshot
  };
}

function health() {
  const pool = POOL.metrics?.() || {};
  const cluster = CLUSTER.metrics?.() || STATE.snapshot || { workers: 0, sessions: 0 };

  return {
    booted: STATE.booted,
    pool,
    cluster,
    ok: STATE.booted && pool.workers > 0 && cluster.workers > 0
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

function request(cmd) {
  if (!STATE.booted) throw new Error('NOT_BOOTED');

  return CLUSTER.request
    ? CLUSTER.request(cmd)
    : POOL.request(cmd);
}

module.exports = { start, health, verify, request };
