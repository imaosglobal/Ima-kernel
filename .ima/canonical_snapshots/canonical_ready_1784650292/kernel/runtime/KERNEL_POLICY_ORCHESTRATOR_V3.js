const crypto = require('crypto');
const POOL = require('./KERNEL_EXECUTION_POOL_V1');
const TX = require('./KERNEL_TRANSACTION_ENGINE_V1');

POOL.start();

// --------------------
// POLICY ENGINE
// --------------------

const POLICY = {
  allow: ['WRITE_FILE', 'GET_STATE', 'INSPECT'],
  deny: ['DELETE_FILE', 'FORMAT_DISK']
};

function checkPolicy(cmd){
  if(!cmd || !cmd.type) return {ok:false, reason:'missing_type'};

  if(POLICY.deny.includes(cmd.type)){
    return {ok:false, reason:'blocked_by_policy'};
  }

  if(!POLICY.allow.includes(cmd.type)){
    return {ok:false, reason:'not_in_allowlist'};
  }

  return {ok:true};
}

// --------------------
// ORCHESTRATION GRAPH
// --------------------

const GRAPH = {};

function add(cmd, deps=[]){
  const id = crypto.randomUUID();
  GRAPH[id] = {
    id,
    cmd,
    deps,
    status:'pending'
  };
  return id;
}

function canRun(node){
  return node.deps.every(d => GRAPH[d]?.status === 'done');
}

function run(){
  const state = TX.load();

  let progress = true;
  let rounds = 0;

  while(progress && rounds < 50){
    progress = false;
    rounds++;

    for(const id in GRAPH){
      const node = GRAPH[id];
      if(node.status !== 'pending') continue;
      if(!canRun(node)) continue;

      const policy = checkPolicy(node.cmd);
      if(!policy.ok){
        node.status = 'blocked';
        continue;
      }

      const tx = TX.begin(state, node.cmd);

      try {
        const res = POOL.request(node.cmd);

        TX.markCommitted(state, tx.id, res);
        node.status = 'done';

        progress = true;

      } catch(e){
        TX.markFailed(state, tx.id, e.message);
        node.status = 'failed';
      }
    }
  }

  TX.save(state);

  return {
    status:'complete',
    rounds
  };
}

function inspect(){
  const s = TX.load();
  return {
    graph: GRAPH,
    tx: s
  };
}

module.exports = { add, run, inspect };
