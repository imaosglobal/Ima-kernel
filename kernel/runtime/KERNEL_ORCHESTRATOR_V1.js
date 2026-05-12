const fs = require('fs');
const crypto = require('crypto');

const EXEC = require('./KERNEL_EXECUTION_LAYER_V2');

const STATE_PATH = './runtime/.orchestrator_state.json';

function load(){
  try { return JSON.parse(fs.readFileSync(STATE_PATH,'utf8')); }
  catch {
    return {
      graph: {},
      history: [],
      snapshots: {}
    };
  }
}

function save(s){
  fs.writeFileSync(STATE_PATH, JSON.stringify(s,null,2));
}

function hash(obj){
  return crypto.createHash('sha256').update(JSON.stringify(obj)).digest('hex');
}

// -----------------------------
// DAG BUILDER
// -----------------------------

function addNode(state, node){
  const id = hash(node);

  state.graph[id] = {
    ...node,
    id,
    status: 'pending',
    deps: node.deps || []
  };

  return id;
}

// -----------------------------
// TOPOLOGICAL EXECUTION
// -----------------------------

function canRun(state, node){
  return node.deps.every(d => {
    const dep = state.graph[d];
    return dep && dep.status === 'done';
  });
}

// -----------------------------
// SNAPSHOT SYSTEM
// -----------------------------

function snapshot(state, id){
  state.snapshots[id] = JSON.parse(JSON.stringify(state.graph));
}

// -----------------------------
// ROLLBACK
// -----------------------------

function rollback(state, toId){
  if(!state.snapshots[toId]) return {status:'no_snapshot'};

  state.graph = JSON.parse(JSON.stringify(state.snapshots[toId]));
  return {status:'rolled_back', toId};
}

// -----------------------------
// RUN ENGINE
// -----------------------------

function run(){

  const state = load();

  let progress = true;
  let iterations = 0;

  while(progress && iterations < 50){

    progress = false;
    iterations++;

    for(const id of Object.keys(state.graph)){
      const node = state.graph[id];

      if(node.status !== 'pending') continue;
      if(!canRun(state, node)) continue;

      try{

        const res = EXEC.execute(node.cmd);

        state.history.push({id, res});
        node.status = 'done';

        snapshot(state, id);

        progress = true;

      }catch(e){
        node.status = 'failed';
        node.error = e.message;
      }
    }

    save(state);
  }

  return {
    status: 'complete',
    iterations
  };
}

// -----------------------------
// API
// -----------------------------

function add(cmd, deps=[]){
  const state = load();
  const id = addNode(state, {cmd, deps});
  save(state);
  return id;
}

function status(){
  const s = load();
  return {
    nodes: Object.keys(s.graph).length,
    history: s.history.length
  };
}

module.exports = {
  add,
  run,
  status,
  rollback
};
