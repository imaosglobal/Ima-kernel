const fs = require('fs');

const STATE_PATH = './runtime/.tx_state.json';
const LOCK_PATH  = './runtime/.tx_lock.json';

// --------------------
// atomic lock
// --------------------

function lock(){
  try {
    if(fs.existsSync(LOCK_PATH)) return false;
    fs.writeFileSync(LOCK_PATH, String(Date.now()));
    return true;
  } catch {
    return false;
  }
}

function unlock(){
  try { fs.unlinkSync(LOCK_PATH); } catch {}
}

// --------------------
// safe load (always fresh)
// --------------------

function load(){
  try {
    return JSON.parse(fs.readFileSync(STATE_PATH,'utf8'));
  } catch {
    return { sessions:{} };
  }
}

// --------------------
// atomic save
// --------------------

function save(state){

  while(!lock()) {}

  try {
    fs.writeFileSync(STATE_PATH, JSON.stringify(state,null,2));
  } finally {
    unlock();
  }
}

// --------------------
// session ops
// --------------------

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

  if(session.executed[node.id]){
    return {skipped:true};
  }

  try {

    const fs = require('fs');

    if(node.cmd.type === 'WRITE_FILE'){
      fs.writeFileSync(node.cmd.file, node.cmd.content);
    }

    session.executed[node.id] = true;
    session.history.push({id:node.id, ok:true});

    return {ok:true};

  } catch(e){

    session.failed = true;
    return {ok:false, error:e.message};

  }
}

module.exports = {
  load,
  save,
  newSession,
  runNode
};
