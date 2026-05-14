const POOL = require('./KERNEL_EXECUTION_POOL_V1');
const TX = require('./KERNEL_TRANSACTION_ENGINE_V1');

POOL.start();

function validate(req){
  if(!req || !req.type){
    return {ok:false, reason:'missing_type'};
  }
  return {ok:true};
}

function request(req){
  const state = TX.load();

  const v = validate(req);
  if(!v.ok){
    const tx = TX.begin(state, req);
    TX.markFailed(state, tx.id, v.reason);
    TX.save(state);
    return {status:'rejected', tx:tx.id};
  }

  const tx = TX.begin(state, req);

  try {
    const res = POOL.request(req);

    TX.markCommitted(state, tx.id, res);
    TX.save(state);

    return {
      status:'ok',
      tx: tx.id,
      result: res
    };

  } catch(e){
    TX.markFailed(state, tx.id, e.message);
    TX.save(state);

    return {
      status:'error',
      tx: tx.id,
      reason: e.message
    };
  }
}

function metrics(){
  const s = TX.load();
  return {
    transactions: Object.keys(s.transactions).length,
    committed: s.committed.length,
    failed: s.failed.length
  };
}

module.exports = { request, metrics };
