const BUS = require('./KERNEL_EVENT_BUS_V2');
const SNAP = require('./KERNEL_SNAPSHOT_ENGINE_V1');

function stateAt(timestamp){

  const events = BUS.all().filter(e => e.ts <= timestamp);

  const state = {
    files: {},
    tx: []
  };

  for(const e of events){
    if(e.type === 'REQUEST'){
      state.tx.push(e);
    }
  }

  return state;
}

function timeline(){
  const events = BUS.all();

  return events.map(e => ({
    ts: e.ts,
    type: e.type,
    id: e.id
  }));
}

function snapshotHistory(){
  return SNAP.latest();
}

module.exports = {
  stateAt,
  timeline,
  snapshotHistory
};
