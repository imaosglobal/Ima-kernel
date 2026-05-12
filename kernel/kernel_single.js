'use strict';

const POOL = require('./runtime/KERNEL_EXECUTION_POOL_V1.js');
const CLUSTER = require('./runtime/KERNEL_CLUSTER_MASTER_V8.js');

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
