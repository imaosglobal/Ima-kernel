const UNIFIED = require('./KERNEL_UNIFIED_RUNTIME_V1');
const BUS = require('./KERNEL_EVENT_BUS_V2');
const CLUSTER = require('./KERNEL_CLUSTER_MASTER_V8');

const STATE = {
  running: false,
  tick: 0
};

function start(options = {}){

  if(STATE.running) return {status:'already_running'};
  STATE.running = true;

  // optional cluster start
  if(CLUSTER && typeof CLUSTER.start === 'function'){
    try { CLUSTER.start(); } catch(e){}
  }

  // main loop
  const interval = options.interval || 1000;

  const timer = setInterval(() => {

    STATE.tick++;

    // emit heartbeat
    if(BUS.emit){
      BUS.emit('tick', { tick: STATE.tick });
    }

    // optional scheduled work
    if(options.onTick){
      try { options.onTick(STATE.tick, UNIFIED); } catch(e){}
    }

    // stop guard
    if(options.maxTicks && STATE.tick >= options.maxTicks){
      stop();
    }

  }, interval);

  STATE.timer = timer;

  return { status:'started', interval };
}

function stop(){
  if(STATE.timer){
    clearInterval(STATE.timer);
    STATE.timer = null;
  }
  STATE.running = false;
  return { status:'stopped', ticks: STATE.tick };
}

function submit(cmd){
  return UNIFIED.process(cmd);
}

function metrics(){
  return {
    ...STATE,
    unified: UNIFIED.metrics?.()
  };
}

module.exports = {
  start,
  stop,
  submit,
  metrics
};
