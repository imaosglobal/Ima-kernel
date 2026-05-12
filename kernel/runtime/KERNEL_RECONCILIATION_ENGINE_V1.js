const fs = require('fs');

const ORCH = require('./KERNEL_ORCHESTRATOR_V2');
const TX = require('./KERNEL_TRANSACTION_LAYER_V2');
const POOL = require('./KERNEL_EXECUTION_POOL_V1');

function loadSnapshot(){
  try {
    return JSON.parse(fs.readFileSync('./runtime/.kernel_snapshot.json','utf8'));
  } catch {
    return null;
  }
}

// ----------------------
// BUILD UNIFIED VIEW
// ----------------------
function buildView(){
  const snapshot = loadSnapshot();
  const tx = TX.load ? TX.load() : {};
  const metrics = POOL.metrics ? POOL.metrics() : {};

  return {
    snapshot,
    tx,
    pool: metrics,
    graph: ORCH.inspect ? ORCH.inspect() : null
  };
}

// ----------------------
// DETECT DRIFT
// ----------------------
function detectDrift(view){
  const drift = [];

  const graph = view.graph?.graph || {};
  const txNodes = view.tx?.transactions || {};

  // graph vs tx mismatch
  for(const id in graph){
    const node = graph[id];

    const txMatch = Object.values(txNodes).find(t =>
      t.cmd?.file === node.cmd?.file
    );

    if(node.status === 'done' && (!txMatch || txMatch.status !== 'committed')){
      drift.push({
        type:'GRAPH_TX_MISMATCH',
        id
      });
    }
  }

  return drift;
}

// ----------------------
// RECONCILE
// ----------------------
function reconcile(){
  const view = buildView();
  const drift = detectDrift(view);

  let fixed = 0;

  for(const d of drift){
    if(d.type === 'GRAPH_TX_MISMATCH'){
      const g = view.graph.graph[d.id];
      if(g){
        g.status = 'pending';
        fixed++;
      }
    }
  }

  return {
    drift: drift.length,
    fixed,
    consistent: drift.length === 0
  };
}

module.exports = {
  buildView,
  detectDrift,
  reconcile
};
