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

// ---------------- EVENT BUS ----------------

class EventBus{

  constructor(){
    this.events=[];
  }

  emit(type,data){
    this.events.push({
      t:Date.now(),
      type,
      data
    });

    if(this.events.length>500)
      this.events.shift();
  }

  get(type){
    return this.events.filter(e=>e.type===type);
  }
}

// ---------------- MEMORY ----------------

const MEM_FILE='memory/v6.json';

function load(){
  try{return JSON.parse(fs.readFileSync(MEM_FILE));}
  catch{
    return {
      state:"init",
      cycles:0,
      failures:0,
      score:0,
      history:[]
    };
  }
}

function save(m){
  fs.mkdirSync(path.dirname(MEM_FILE),{recursive:true});
  fs.writeFileSync(MEM_FILE,JSON.stringify(m,null,2));
}

// ---------------- AGENTS ----------------

class Agent{

  constructor(name,fn){
    this.name=name;
    this.fn=fn;
  }

  async run(ctx,bus){

    try{
      await this.fn(ctx,bus);
      ctx.score+=1;
    }catch(e){
      ctx.failures++;
    }

  }
}

// ---------------- SYSTEM AGENTS ----------------

const agents=[

  new Agent("sync", async ()=>{
    run("git pull --rebase || true");
  }),

  new Agent("build", async ()=>{
    run("node system/final_autonomous_pipeline.js");
  }),

  new Agent("health", async (ctx)=>{
    ctx.health = run("node runtime/autonomous_runtime.js --check") !== null;
  }),

  new Agent("repair", async (ctx,bus)=>{
    if(ctx.failures>0){
      bus.emit("repair","triggered");
      run("node system/final_autonomous_pipeline.js");
    }
  }),

  new Agent("adaptive", async (ctx,bus)=>{

    // pseudo-learning: score history
    const last = ctx.history.slice(-5);

    if(last.length && last.every(x=>x.score<2)){
      bus.emit("adapt","low-performance");
      ctx.failures++;
    }

  })

];

// ---------------- DECISION ENGINE ----------------

function decide(ctx){

  if(ctx.failures>3) return "RECOVERY";
  if(!ctx.health) return "HEAL";
  if(ctx.score<2) return "BOOST";

  return "NORMAL";
}

// ---------------- MAIN LOOP ----------------

async function loop(){

  console.log("IMA v6 DISTRIBUTED RUNTIME STARTED");

  const bus=new EventBus();
  let mem=load();

  while(true){

    mem.cycles++;

    const ctx={
      score:0,
      failures:0,
      health:true,
      history:mem.history
    };

    for(const a of agents){
      await a.run(ctx,bus);
    }

    const decision=decide(ctx);

    mem.state=decision;
    mem.score=ctx.score;
    mem.failures+=ctx.failures;

    mem.history.push({
      t:Date.now(),
      decision,
      score:ctx.score
    });

    if(mem.history.length>300)
      mem.history.shift();

    bus.emit("cycle",decision);

    // ACTIONS

    if(decision==="HEAL"){
      run("node system/final_autonomous_pipeline.js");
    }

    if(decision==="RECOVERY"){
      run("git reset --hard || true");
      run("node system/final_autonomous_pipeline.js");
    }

    if(decision==="BOOST"){
      run("node system/final_autonomous_pipeline.js");
    }

    save(mem);

    await sleep(8000);
  }
}

loop();
