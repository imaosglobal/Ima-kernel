const POOL = require('./KERNEL_EXECUTION_POOL_V1');
const TX = require('./KERNEL_TRANSACTION_ENGINE_V1');
const BUS = require('./KERNEL_EVENT_BUS_V1');

POOL.start();

function request(cmd){

  // 1. event log ראשון (source of truth)
  const event = BUS.emit('REQUEST', cmd);

  const state = TX.load();
  const tx = TX.begin(state, cmd);

  try{
    const res = POOL.request(cmd);

    TX.markCommitted(state, tx.id, res);
    TX.save(state);

    BUS.emit('COMMIT', { tx: tx.id, res });

    return {
      status:'ok',
      tx: tx.id,
      event: event.id,
      result: res
    };

  }catch(e){
    TX.markFailed(state, tx.id, e.message);
    TX.save(state);

    BUS.emit('FAIL', { tx: tx.id, error: e.message });

    return {
      status:'error',
      tx: tx.id,
      event: event.id,
      error: e.message
    };
  }
}

function metrics(){
  const s = TX.load();
  const events = BUS.all();

  return {
    transactions: Object.keys(s.transactions).length,
    events: events.length,
    committed: s.committed.length,
    failed: s.failed.length
  };
}

module.exports = { request, metrics };
