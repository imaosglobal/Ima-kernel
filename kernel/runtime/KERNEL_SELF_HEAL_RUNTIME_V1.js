const fs = require('fs');
const UNIFIED = require('./KERNEL_UNIFIED_RUNTIME_V1');

const SNAP_PATH = './runtime/.kernel_snapshot.json';

const STATE = {
  running: false,
  ticks: 0,
  failures: 0,
  recovered: false
};

// ----------------------
// SNAPSHOT
// ----------------------
function snapshot(extra = {}){
  const data = {
    ticks: STATE.ticks,
    failures: STATE.failures,
    unified: UNIFIED.metrics ? UNIFIED.metrics() : {},
    time: Date.now(),
    ...extra
  };

  fs.writeFileSync(SNAP_PATH, JSON.stringify(data, null, 2));
  return data;
}

// ----------------------
// RESTORE
// ----------------------
function restore(){
  try {
    if(!fs.existsSync(SNAP_PATH)){
      return { restored:false };
    }

    const data = JSON.parse(fs.readFileSync(SNAP_PATH,'utf8'));

    STATE.ticks = data.ticks || 0;
    STATE.failures = data.failures || 0;
    STATE.recovered = true;

    return { restored:true, data };
  } catch(e){
    return { restored:false, error:e.message };
  }
}

// ----------------------
// HEAL EXECUTION
// ----------------------
function heal(cmd){
  // retry logic (simple)
  try {
    return UNIFIED.process(cmd);
  } catch(e){
    STATE.failures++;
    return { status:'healed_failed', error:e.message };
  }
}

// ----------------------
// MAIN LOOP WRAPPER
// ----------------------
function start(options = {}){

  const restored = restore();

  STATE.running = true;

  const interval = options.interval || 1000;

  const timer = setInterval(() => {

    STATE.ticks++;

    // snapshot every tick
    snapshot();

    // optional workload
    if(options.onTick){
      try {
        options.onTick({
          tick: STATE.ticks,
          heal,
          unified: UNIFIED
        });
      } catch(e){
        STATE.failures++;
      }
    }

    if(options.maxTicks && STATE.ticks >= options.maxTicks){
      stop();
    }

  }, interval);

  STATE.timer = timer;

  return {
    status:'started',
    restored,
    interval
  };
}

// ----------------------
function stop(){
  if(STATE.timer){
    clearInterval(STATE.timer);
  }
  STATE.running = false;
  return { status:'stopped', ticks: STATE.ticks };
}

// ----------------------
function metrics(){
  return {
    ...STATE,
    unified: UNIFIED.metrics ? UNIFIED.metrics() : {}
  };
}

module.exports = {
  start,
  stop,
  metrics,
  snapshot,
  restore,
  heal
};
