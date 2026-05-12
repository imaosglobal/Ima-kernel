const fs = require('fs');

const STATE_FILE = './runtime/.kernel_consolidation.json';

const REGISTRY = {
  eventBus: [
    './KERNEL_EVENT_BUS_V2.js',
    './KERNEL_EVENT_BUS_V1.js'
  ],
  tx: [
    './KERNEL_TRANSACTION_LAYER_V2.js',
    './KERNEL_TRANSACTION_ENGINE_V1.js'
  ],
  orchestrator: [
    './KERNEL_POLICY_ORCHESTRATOR_V3.js',
    './KERNEL_ORCHESTRATOR_V2.js'
  ],
  execution: [
    './KERNEL_EXECUTION_LAYER_V2.js',
    './KERNEL_EXECUTION_POOL_V1.js'
  ],
  cluster: [
    './KERNEL_CLUSTER_MASTER_V8.js'
  ]
};

function load(){
  try { return JSON.parse(fs.readFileSync(STATE_FILE,'utf8')); }
  catch {
    return {
      active: {},
      disabled: [],
      timestamp: Date.now()
    };
  }
}

function save(s){
  fs.writeFileSync(STATE_FILE, JSON.stringify(s,null,2));
}

function pickLatest(versions){
  // heuristic: last in list = canonical
  return versions[versions.length - 1];
}

function consolidate(){
  const state = load();

  for(const key in REGISTRY){
    const list = REGISTRY[key];

    const active = pickLatest(list);
    state.active[key] = active;

    // mark others as disabled
    state.disabled.push(...list.slice(0, -1));
  }

  state.timestamp = Date.now();
  save(state);

  return state;
}

function inspect(){
  return load();
}

module.exports = {
  consolidate,
  inspect
};
