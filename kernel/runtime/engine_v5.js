const fs=require('fs');
const cp=require('child_process');
const path=require('path');
const crypto=require('crypto');

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

function sha(data){
  return crypto.createHash('sha256').update(data).digest('hex');
}

// ---------------- STATE ----------------

const STATE_FILE='memory/v5_state.json';

function load(){
  try{return JSON.parse(fs.readFileSync(STATE_FILE));}
  catch{
    return {
      cycles:0,
      mode:"INIT",
      agents:{},
      history:[],
      failures:0
    };
  }
}

function save(s){
  fs.mkdirSync(path.dirname(STATE_FILE),{recursive:true});
  fs.writeFileSync(STATE_FILE,JSON.stringify(s,null,2));
}

// ---------------- AGENTS ----------------

class Agent{

  constructor(name,fn){
    this.name=name;
    this.fn=fn;
    this.status="idle";
  }

  async run(ctx){
    try{
      this.status="running";
      await this.fn(ctx);
      this.status="ok";
    }catch(e){
      this.status="fail";
      ctx.failures++;
    }
  }

}

// ---------------- ORCHESTRATOR ----------------

class Orchestrator{

  constructor(){

    this.agents=[

      new Agent("sync", async ()=>{
        run('git pull --rebase || true');
      }),

      new Agent("build", async ()=>{
        run('node system/final_autonomous_pipeline.js');
      }),

      new Agent("health", async (ctx)=>{
        const ok = run('node server.js --check') !== null;
        ctx.health=ok;
      }),

      new Agent("repair", async (ctx)=>{
        if(ctx.failures>0){
          run('node system/final_autonomous_pipeline.js');
        }
      })

    ];
  }

  async step(ctx){

    for(const a of this.agents){
      await a.run(ctx);
    }

  }
}

// ---------------- DECISION ENGINE ----------------

function decide(ctx){

  if(ctx.failures>3) return "RECOVERY";

  if(!ctx.health) return "HEAL";

  return "NORMAL";
}

// ---------------- MEMORY ----------------

function remember(state,msg){
  state.history.push({
    t:Date.now(),
    msg
  });

  if(state.history.length>300)
    state.history.shift();
}

// ---------------- LOOP ----------------

async function loop(){

  console.log("IMA v5 MULTI-AGENT SYSTEM STARTED");

  const orchestrator=new Orchestrator();

  let state=load();

  while(true){

    state.cycles++;

    const ctx={
      failures:0,
      health:true
    };

    await orchestrator.step(ctx);

    const decision=decide(ctx);

    state.mode=decision;
    state.failures+=ctx.failures;

    remember(state,decision);

    if(decision==="HEAL"){
      run('node system/final_autonomous_pipeline.js');
    }

    if(decision==="RECOVERY"){
      run('git reset --hard || true');
      run('node system/final_autonomous_pipeline.js');
    }

    save(state);

    await sleep(10000);
  }
}

loop();
