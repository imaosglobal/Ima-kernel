const POOL = require('./KERNEL_EXECUTION_POOL_V1');
const CLUSTER = require('./KERNEL_CLUSTER_MASTER_V8');
const LOG = require('./SYSTEM_EVENT_LOG_RUNTIME_V1');
const NORM = require('./SYSTEM_EVENT_SCHEMA_NORMALIZER_V1');
const SYNC = require('./SYSTEM_CLUSTER_STATE_SYNC_V1');

let STATE = {
  booted: false,
  clusterMap: new Map()
};

function rebuildCluster() {
  const replay = LOG.replay?.((cmd) => POOL.request(cmd)) || { results: [] };
  const events = replay.results || [];

  for (const e of events) {
    const n = NORM.normalize(e);
    if (!n) continue;

    if (!STATE.clusterMap.has(n.session)) {
      STATE.clusterMap.set(n.session, { nodes: [] });
    }

    STATE.clusterMap.get(n.session).nodes.push(n);
  }

  return {
    sessions: STATE.clusterMap.size,
    nodes: [...STATE.clusterMap.values()].reduce((a, s) => a + (s.nodes?.length || 0), 0)
  };
}

function start() {
  console.log('[BRIDGE] booting...');

  if (STATE.booted) {
    return { status: 'already_booted' };
  }

  STATE.booted = true;

  POOL.start?.();
  CLUSTER.start?.();

  const clusterState = rebuildCluster();

  // 🔴 חדש: הזרקת state ל-cluster runtime
  try {
    if (SYNC?.sync) {
      SYNC.sync(STATE.clusterMap);
    }
  } catch (e) {
    console.log('[SYNC ERROR]', e.message);
  }

  const result = {
    status: 'cluster_rehydrated',
    clusterState,
    pool: POOL.metrics?.(),
    cluster: CLUSTER.metrics?.()
  };

  console.log('[BRIDGE RESULT]', result);

  return result;
}

function verify() {
  const pool = POOL.metrics?.() || {};
  const cluster = CLUSTER.metrics?.() || {};

  const ok =
    pool.workers > 0 &&
    cluster.workers > 0 &&
    STATE.clusterMap.size > 0;

  const result = {
    ok,
    clusterSessions: STATE.clusterMap.size,
    pool,
    cluster
  };

  console.log('[VERIFY]', result);
  return result;
}

if (require.main === module) {
  start();
  setTimeout(() => verify(), 1500);
}

module.exports = { start, verify };
