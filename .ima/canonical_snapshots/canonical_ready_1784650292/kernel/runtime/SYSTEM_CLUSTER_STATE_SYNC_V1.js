const CLUSTER = require('./KERNEL_CLUSTER_MASTER_V8');

function sync(stateMap) {
  if (!CLUSTER.injectState) {
    throw new Error('CLUSTER missing injectState() hook');
  }

  const flat = [];

  for (const [session, data] of stateMap.entries()) {
    flat.push({
      session,
      nodes: data.nodes || []
    });
  }

  return CLUSTER.injectState(flat);
}

module.exports = { sync };
