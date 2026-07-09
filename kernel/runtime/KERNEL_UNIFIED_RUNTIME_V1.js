const ADAPTER = require('./KERNEL_EXECUTION_ADAPTER_V1');
const TX = require('./KERNEL_TRANSACTION_LAYER');
const POLICY = require('./KERNEL_POLICY_ORCHESTRATOR_V3');
const BUS = require('./KERNEL_EVENT_BUS_V2');

const STATE = {
  running: false,
  processed: 0,
  failed: 0
};

function process(cmd){

  // 1. policy gate
  const policy = POLICY.checkPolicy ? POLICY.checkPolicy(cmd) : {ok:true};
  if(policy.ok === false){
    STATE.failed++;
    return { status:'blocked', reason: policy.reason };
  }

  // 2. tx begin
  const txState = TX.load ? TX.load() : {};
  const tx = TX.begin ? TX.begin(txState, cmd) : null;

  try {

    // 3. execution
    const res = ADAPTER.execute(cmd);

    // 4. tx commit
    if(tx && TX.markCommitted){
      TX.markCommitted(txState, tx.id, res);
      TX.save(txState);
    }

    // 5. event emit
    if(BUS.emit){
      BUS.emit('executed', { cmd, res });
    }

    STATE.processed++;

    return res;

  } catch(e){

    STATE.failed++;

    if(tx && TX.markFailed){
      TX.markFailed(txState, tx.id, e.message);
      TX.save(txState);
    }

    return { status:'failed', error:e.message };
  }
}

function runBatch(cmds=[]){
  const results = [];

  for(const cmd of cmds){
    results.push(process(cmd));
  }

  return {
    processed: STATE.processed,
    failed: STATE.failed,
    results
  };
}

function metrics(){
  return { ...STATE };
}

module.exports = {
  process,
  runBatch,
  metrics
};
