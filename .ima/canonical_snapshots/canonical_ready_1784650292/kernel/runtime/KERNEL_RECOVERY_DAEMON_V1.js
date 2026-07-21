const fs = require('fs');
const UNIFIED = require('./KERNEL_UNIFIED_RUNTIME_V1');
const SELF_HEAL = require('./KERNEL_SELF_HEAL_RUNTIME_V1');

const SNAP_PATH = './runtime/.kernel_snapshot.json';

const STATE = {
  restored: false,
  running: false
};

// ----------------------
// LOAD SNAPSHOT
// ----------------------
function loadSnapshot(){
  if(!fs.existsSync(SNAP_PATH)){
    return null;
  }

  try {
    return JSON.parse(fs.readFileSync(SNAP_PATH,'utf8'));
  } catch(e){
    return null;
  }
}

// ----------------------
// REHYDRATE SYSTEM
// ----------------------
function rehydrate(snapshot){
  if(!snapshot) return { ok:false };

  // restore unified runtime if possible
  if(UNIFIED && UNIFIED._hydrate){
    UNIFIED._hydrate(snapshot.unified || {});
  }

  return { ok:true };
}

// ----------------------
// REPLAY SAFE STATE
// ----------------------
function replay(snapshot){
  if(!snapshot) return { replayed:0 };

  let replayed = 0;

  // אם יש pending או partial state בעתיד – כאן מריצים שוב
  if(snapshot.pendingCommands){
    for(const cmd of snapshot.pendingCommands){
      try{
        SELF_HEAL.heal(cmd);
        replayed++;
      }catch(e){}
    }
  }

  return { replayed };
}

// ----------------------
// START RECOVERY
// ----------------------
function start(){
  const snapshot = loadSnapshot();

  if(!snapshot){
    STATE.restored = false;
    return { status:'no_snapshot' };
  }

  const r1 = rehydrate(snapshot);
  const r2 = replay(snapshot);

  STATE.restored = true;

  return {
    status:'recovered',
    rehydrated: r1.ok,
    replayed: r2.replayed
  };
}

// ----------------------
module.exports = {
  start
};
