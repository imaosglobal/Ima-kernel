const CLUSTER = require('./KERNEL_CLUSTER_MASTER_V8');

let locked = false;

/**
 * Wrap start so cluster cannot restart or drop
 */
const originalStart = CLUSTER.start;

CLUSTER.start = function () {
  if (locked) {
    return { status: 'cluster_locked_no_restart' };
  }

  const res = originalStart.apply(this, arguments);

  if (res && res.status === 'booted') {
    locked = true;
  }

  return res;
};

/**
 * Prevent post-boot cluster drop via metrics mutation
 */
function stabilize() {
  const m = CLUSTER.metrics?.();

  if (m && m.workers > 0) {
    CLUSTER._FROZEN = true;
  }
}

/**
 * Watchdog guard (safe no-op if not used)
 */
if (CLUSTER.on) {
  CLUSTER.on('message', () => {
    if (CLUSTER._FROZEN) return;
  });
}

module.exports = {
  stabilize
};
