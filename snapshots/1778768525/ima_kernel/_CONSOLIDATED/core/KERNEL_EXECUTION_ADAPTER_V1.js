const POOL = require('./KERNEL_EXECUTION_POOL_V1');

function execute(cmd){
  if(!cmd || !cmd.type){
    return { status: 'error', reason: 'missing_cmd' };
  }

  // translate contract -> actual runtime API
  const res = POOL.request(cmd);

  return {
    status: 'executed',
    result: res
  };
}

function start(){
  if(typeof POOL.start === 'function'){
    return POOL.start();
  }
}

function metrics(){
  return POOL.metrics ? POOL.metrics() : {};
}

function inspect(session){
  return POOL.inspect ? POOL.inspect(session) : null;
}

module.exports = {
  execute,
  start,
  metrics,
  inspect
};
