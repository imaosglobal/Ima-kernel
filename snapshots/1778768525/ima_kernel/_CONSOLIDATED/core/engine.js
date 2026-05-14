const fs=require('fs');
const cp=require('child_process');
const path=require('path');

const ROOT=process.cwd();

function run(cmd){
  try {
    return cp.execSync(cmd,{
      cwd:ROOT,
      stdio:'pipe',
      shell:true
    }).toString().trim();
  } catch(e){
    return null;
  }
}

function sleep(ms){
  return new Promise(r=>setTimeout(r,ms));
}

// ---------------- MEMORY ----------------

const MEM_FILE='memory/runtime_state.json';

function load(){
  try {
    return JSON.parse(fs.readFileSync(MEM_FILE));
  } catch(e){
    return {
      cycles:0,
      failures:0,
      lastGood:null,
      logs:[]
    };
  }
}

function save(m){
  fs.mkdirSync(path.dirname(MEM_FILE),{recursive:true});
  fs.writeFileSync(MEM_FILE,JSON.stringify(m,null,2));
}

// ---------------- CORE ACTIONS ----------------

function gitSync(){
  run('git pull --rebase || true');
}

function runPipeline(){
  return run('node system/final_autonomous_pipeline.js');
}

function healthCheck(){
  const r = run('node runtime/autonomous_runtime.js --check');
  return r !== null;
}

function log(m, msg){
  m.logs.push({t:Date.now(),msg});
  if(m.logs.length>200) m.logs.shift();
}

// ---------------- ENGINE LOOP ----------------

async function loop(){

  console.log('IMA RUNTIME ENGINE STARTED');

  let state = load();

  while(true){

    state.cycles++;

    try {

      // 1. sync
      gitSync();

      // 2. run pipeline
      runPipeline();

      // 3. health check
      const ok = healthCheck();

      if(ok){
        state.lastGood = Date.now();
      } else {
        state.failures++;
        log(state,"HEALTH FAIL → RECOVERY");
        runPipeline();
      }

      // 4. auto-heal logic
      if(state.failures > 5){
        log(state,"HEAVY FAILURE → RESET STATE");
        state.failures = 0;
      }

      // 5. persist state
      save(state);

      // throttle loop
      await sleep(20000);

    } catch(e){

      state.failures++;
      log(state,"ENGINE CRASH: "+String(e));

      save(state);

      await sleep(10000);

    }
  }
}

loop();
