const fs=require('fs');
const cp=require('child_process');
const path=require('path');

const ROOT=process.cwd();

// ---------------- UTIL ----------------

function run(cmd){
  try{
    return cp.execSync(cmd,{
      cwd:ROOT,
      shell:true,
      stdio:'pipe'
    }).toString().trim();
  }catch(e){
    return null;
  }
}

function sleep(ms){
  return new Promise(r=>setTimeout(r,ms));
}

function load(f,def){
  try{return JSON.parse(fs.readFileSync(f));}
  catch{return def;}
}

function save(f,d){
  fs.mkdirSync(path.dirname(f),{recursive:true});
  fs.writeFileSync(f,JSON.stringify(d,null,2));
}

// ---------------- MEMORY ----------------

const MEMORY_FILE='memory/v3_memory.json';

let memory=load(MEMORY_FILE,{
  events:[],
  knowledge:[],
  goals:["stability","improve","learn"],
  failures:0
});

// ---------------- TOOLS LAYER ----------------

const tools = {

  gitSync: ()=>run('git pull --rebase || true'),

  runPipeline: ()=>run('node system/final_autonomous_pipeline.js'),

  health: ()=>run('node runtime/autonomous_runtime.js --check')!==null,

  listFiles: ()=>run('ls'),

};

// ---------------- SIMPLE "SEMANTIC MEMORY" ----------------

function remember(text){
  memory.knowledge.push({
    t:Date.now(),
    text
  });

  if(memory.knowledge.length>500)
    memory.knowledge.shift();
}

function searchMemory(query){
  return memory.knowledge
    .filter(k=>k.text.includes(query))
    .slice(-5);
}

// ---------------- PLANNER ----------------

function plan(state){

  if(state.failures>3){
    return ["heal","sync","rebuild"];
  }

  if(!state.ok){
    return ["heal"];
  }

  return ["sync","run"];
}

// ---------------- EXECUTOR ----------------

function execute(plan){

  for(const step of plan){

    if(step==="sync") tools.gitSync();
    if(step==="run") tools.runPipeline();
    if(step==="heal") tools.runPipeline();
    if(step==="rebuild") tools.runPipeline();

  }
}

// ---------------- LOOP ----------------

async function loop(){

  console.log("IMA v3 COGNITIVE ENGINE STARTED");

  while(true){

    const state={
      ok:tools.health(),
      failures:memory.failures
    };

    memory.events.push({
      t:Date.now(),
      state
    });

    const planSteps=plan(state);

    execute(planSteps);

    if(state.ok){
      memory.failures=0;
      remember("system stable");
    }else{
      memory.failures++;
      remember("system instability detected");
    }

    save(MEMORY_FILE,memory);

    await sleep(12000);
  }
}

loop();
