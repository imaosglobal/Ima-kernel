const fs=require('fs');
const cp=require('child_process');
const path=require('path');

const ROOT=process.cwd();

// ---------------- UTIL ----------------

function run(cmd){
  try {
    return cp.execSync(cmd,{
      cwd:ROOT,
      shell:true,
      stdio:'pipe'
    }).toString().trim();
  } catch(e){
    return null;
  }
}

function sleep(ms){
  return new Promise(r=>setTimeout(r,ms));
}

function loadJSON(f,def){
  try { return JSON.parse(fs.readFileSync(f)); }
  catch { return def; }
}

function saveJSON(f,data){
  fs.mkdirSync(path.dirname(f),{recursive:true});
  fs.writeFileSync(f,JSON.stringify(data,null,2));
}

// ---------------- MEMORY ----------------

const MEM_FILE='memory/v2_memory.json';

let memory = loadJSON(MEM_FILE,{
  goals:[],
  events:[],
  failures:0,
  cycles:0,
  lastHealth:true
});

// ---------------- GOAL ENGINE ----------------

function updateGoals(){

  // בסיס התנהגותי (ניתן להרחיב)
  const baseGoals = [
    "keep_system_alive",
    "fix_failures",
    "sync_repository",
    "run_pipeline"
  ];

  memory.goals = baseGoals;
}

// ---------------- DECISION BRAIN ----------------

function decide(){

  if(memory.failures > 5){
    return "RECOVERY_MODE";
  }

  if(!memory.lastHealth){
    return "HEAL";
  }

  return "NORMAL";
}

// ---------------- ACTIONS ----------------

function sync(){
  run('git pull --rebase || true');
}

function pipeline(){
  run('node system/final_autonomous_pipeline.js');
}

function health(){
  return run('node server.js --check') !== null;
}

function heal(){
  pipeline();
  sync();
}

// ---------------- EVENT SYSTEM ----------------

function emit(event){
  memory.events.push({
    t:Date.now(),
    event
  });

  if(memory.events.length > 200)
    memory.events.shift();
}

// ---------------- PLUGIN LOADER ----------------

function loadPlugins(){
  const dir='plugins';

  if(!fs.existsSync(dir)) return;

  for(const f of fs.readdirSync(dir)){
    try {
      require(path.join(ROOT,dir,f));
    } catch(e){}
  }
}

// ---------------- MAIN LOOP ----------------

async function loop(){

  console.log("IMA RUNTIME ENGINE v2 STARTED");

  loadPlugins();

  while(true){

    memory.cycles++;

    updateGoals();

    sync();

    pipeline();

    memory.lastHealth = health();

    const decision = decide();

    emit(decision);

    if(decision === "RECOVERY_MODE"){
      memory.failures++;
      heal();
    }

    if(decision === "HEAL"){
      heal();
    }

    if(memory.lastHealth){
      memory.failures = 0;
    }

    saveJSON(MEM_FILE,memory);

    await sleep(15000);
  }
}

loop();
