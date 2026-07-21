const POOL = require('./KERNEL_EXECUTION_POOL_V1');
const CLUSTER = require('./KERNEL_CLUSTER_MASTER_V8');
const LOG = require('./SYSTEM_EVENT_LOG_RUNTIME_V1');

let STATE = {
  booted: false,
  clusterMap: new Map(),
  sessionMap: new Map()
};

// --------------------
// BUILD CLUSTER FROM LOG
// --------------------
function rebuildCluster() {
  const replay = LOG.replay((cmd) => POOL.request(cmd));

  const graph = replay.results || [];

  for (const item of graph) {
    const session = item?.cmd?.session || 'unknown';
    const node = item?.cmd?.nodeId || item?.node || null;

    if (!session || !node) continue;

    if (!STATE.clusterMap.has(session)) {
      STATE.clusterMap.set(session, {
        nodes: [],
        status: 'rehydrated'
      });
    }

    STATE.clusterMap.get(session).nodes.push({
      node,
      cmd: item.cmd,
      status: 'restored'
    });
  }

  return {
    sessions: STATE.clusterMap.size,
    nodes: [...STATE.clusterMap.values()].reduce((a, s) => a + s.nodes.length, 0)
  };
}

// --------------------
// BOOT BRIDGE
// --------------------
function start() {
  if (STATE.booted) {
    return { status: 'already_booted' };
  }

  STATE.booted = true;

  POOL.start?.();
  CLUSTER.start?.();

  const clusterState = rebuildCluster();

  return {
    status: 'cluster_rehydrated',
    clusterState,
    pool: POOL.metrics?.(),
    cluster: CLUSTER.metrics?.()
  };
}

// --------------------
// CONSISTENCY CHECK
// --------------------
function verify() {
  const pool = POOL.metrics?.() || {};
  const cluster = CLUSTER.metrics?.() || {};

  const issues = [];

  if (pool.workers !== cluster.workers) {
    issues.push('WORKER_MISMATCH');
  }

  if (STATE.clusterMap.size === 0) {
    issues.push('NO_CLUSTER_STATE_RESTORED');
  }

  return {
    ok: issues.length === 0,
    issues,
    snapshot: {
      pool,
      cluster,
      clusterSessions: STATE.clusterMap.size
    }
  };
}

// --------------------
module.exports = {
  start,
  verify,
  state: () => STATE
};

// SELF TEST
if (require.main === module) {
  console.log('[BRIDGE START]', start());

  setTimeout(() => {
    console.log('[VERIFY]', verify());
  }, 1500);
}
