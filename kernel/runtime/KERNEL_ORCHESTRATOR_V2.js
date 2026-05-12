const fs = require('fs');
const crypto = require('crypto');
const EXEC = require('./KERNEL_EXECUTION_LAYER_V2');

const STATE_PATH = './runtime/.orchestrator_state.json';

function empty(){
  return {
    graph:{},
    history:[],
    snapshots:{},
    executed:{}
  };
}

function normalize(s){
  s = s || {};
  s.graph ||= {};
  s.history ||= [];
  s.snapshots ||= {};
  s.executed ||= {};
  return s;
}

function load(){
  try {
    return normalize(JSON.parse(fs.readFileSync(STATE_PATH,'utf8')));
  } catch {
    return empty();
  }
}

function save(s){
  fs.writeFileSync(STATE_PATH, JSON.stringify(s,null,2));
}

function hash(obj){
  return crypto.createHash('sha256')
    .update(JSON.stringify(obj))
    .digest('hex');
}

// --------------------

function addNode(state, node){
  const id = hash(node);

  state.graph[id] = {
    ...node,
    id,
    status:'pending',
    deps: node.deps || []
  };

  return id;
}

// --------------------

function canRun(state, node){

  if(state.executed[node.id]) return false;

  if(!node.deps || node.deps.length === 0) return true;

  return node.deps.every(d => {
    const dep = state.graph[d];
    return dep && dep.status === 'done';
  });
}

// --------------------

function snapshot(state, id){
  state.snapshots[id] = JSON.parse(JSON.stringify(state));
}

// --------------------

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

        state.executed[id] = true;

        snapshot(state, id);

        progress = true;

      }catch(e){

        node.status = 'failed';
        node.error = e.message;

      }
    }

    save(state);
  }

  return { status:'complete', iterations };
}

function add(cmd, deps=[]){
  const state = load();
  const id = addNode(state, {cmd, deps});
  save(state);
  return id;
}

function status(){
  const s = load();
  return {
    nodes:Object.keys(s.graph).length,
    executed:Object.keys(s.executed).length,
    history:s.history.length
  };
}

function reset(){
  save(empty());
  return {status:'reset'};
}

module.exports = { add, run, status, reset };
