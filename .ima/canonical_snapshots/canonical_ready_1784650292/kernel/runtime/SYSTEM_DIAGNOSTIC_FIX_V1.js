const fs = require('fs');
const path = require('path');

const CLUSTER = require('./KERNEL_CLUSTER_MASTER_V8');
const POOL = require('./KERNEL_EXECUTION_POOL_V1');
const BUS = require('./KERNEL_EVENT_BUS_V2');

function safe(fn, label){
  try {
    return { ok: true, result: fn() };
  } catch (e) {
    return { ok: false, error: `${label}: ${e.message}` };
  }
}

// ----------------------
// FIX: detect broken cluster boot
// ----------------------
function fixClusterStart(){
  if (CLUSTER.__FIXED_BOOT__) return { status: 'already_fixed' };

  // monkey patch safe start wrapper
  const originalStart = CLUSTER.start;

  CLUSTER.start = function(...args){
    try {
      if (typeof args[0] === 'string' && !fs.existsSync(args[0])) {
        console.log('[FIX] invalid worker path ignored, using fallback');
        args[0] = __filename;
      }
      return originalStart.apply(CLUSTER, args);
    } catch (e) {
      console.log('[FIX] cluster start failed, retry suppressed:', e.message);
      return { status: 'failed_safe' };
    }
  };

  CLUSTER.__FIXED_BOOT__ = true;
  return { status: 'cluster_patched' };
}

// ----------------------
// SYSTEM HEALTH
// ----------------------
function health(){
  return {
    pool: safe(() => POOL.metrics?.(), 'pool'),
    cluster: safe(() => CLUSTER.metrics?.(), 'cluster'),
    bus: safe(() => BUS.all?.()?.length, 'bus')
  };
}

// ----------------------
// FULL DIAGNOSTIC
// ----------------------
function run(){
  console.log('[DIAG] starting system scan...');

  const fixes = [];

  // 1. pool check
  try {
    if (POOL.start) POOL.start();
    fixes.push('pool_ok');
  } catch (e) {
    fixes.push('pool_failed');
  }

  // 2. cluster fix + restart
  const clusterFix = fixClusterStart();
  fixes.push(clusterFix.status);

  try {
    if (CLUSTER.start) CLUSTER.start(__filename);
    fixes.push('cluster_restart_attempted');
  } catch (e) {
    fixes.push('cluster_restart_failed');
  }

  // 3. bus check
  try {
    BUS.all?.();
    fixes.push('bus_ok');
  } catch (e) {
    fixes.push('bus_unstable');
  }

  const h = health();

  const clusterWorkers =
    h.cluster.ok ? h.cluster.result?.workers : 0;

  const ok =
    (h.pool.ok && h.pool.result?.workers > 0) &&
    (clusterWorkers > 0);

  return {
    ok,
    fixes,
    health: {
      pool: h.pool,
      cluster: h.cluster,
      bus: h.bus
    }
  };
}

module.exports = {
  run,
  health,
  fixClusterStart
};
