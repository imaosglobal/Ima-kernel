const BUS = require('./KERNEL_EVENT_BUS_V2');

function replay(handler){
  const events = BUS.all();

  const state = {
    files: {},
    tx: []
  };

  for(const e of events){
    if(e.type === 'REQUEST'){
      state.tx.push(e);

      if(handler){
        handler(e, state);
      }
    }
  }

  return {
    replayed: events.length,
    finalState: state
  };
}

module.exports = { replay };
