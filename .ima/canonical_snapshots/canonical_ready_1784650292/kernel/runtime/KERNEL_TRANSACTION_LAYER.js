const fs = require('fs');
const EXEC = require('./KERNEL_EXECUTION_LAYER_V2');

const STATE_PATH = './runtime/.tx_state.json';

function load(){
  try { return JSON.parse(fs.readFileSync(STATE_PATH,'utf8')); }
  catch { return { sessions: {} }; }
}

function save(s){
  fs.writeFileSync(STATE_PATH, JSON.stringify(s,null,2));
}

function newSession(state){
  const id = Date.now().toString();
  state.sessions[id] = {
    graph:{},
    executed:{},
    failed:false,
    history:[]
  };
  return id;
}

function runNode(session, node){
  if(session.executed[node.id]) return {skipped:true};

  try {
    const res = EXEC.execute(node.cmd);
    session.executed[node.id] = true;
    session.history.push({id:node.id, res});
    return {ok:true, res};
  } catch(e){
    session.failed = true;
    return {ok:false, error:e.message};
  }
}

function rollback(session){
  session.graph = {};
  session.executed = {};
  session.history = [];
  session.failed = false;
}

module.exports = {
  load,
  save,
  newSession,
  runNode,
  rollback
};
