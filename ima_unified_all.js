const fs = require("fs");
const { execSync } = require("child_process");

/* ---------- CONFIG ---------- */
const CONFIG_PATH = "./ima_config.json";
const MEMORY_PATH = "./memory.json";

function loadJSON(p, fb){ try { return JSON.parse(fs.readFileSync(p)); } catch { return fb; } }
function saveJSON(p, d){ fs.writeFileSync(p, JSON.stringify(d, null, 2)); }

let config = loadJSON(CONFIG_PATH, {
  version: 1,
  mode: "stable",
  avatar: "default",
  evolution: true,
  weights: { relevance: 0.3, clarity: 0.2, usefulness: 0.3, safety: 0.2 }
});

let memory = loadJSON(MEMORY_PATH, { memory: [] });

/* ---------- CORE KNOWLEDGE ---------- */
const domains = [
  "psychology","finance","health","education","technology",
  "philosophy","religion","science","relationships","daily_life"
];

/* ---------- AGENTS ---------- */
const agents = {
  general: (q)=>`תשובה כללית: ${q}`,
  teacher: (q)=>`הסבר לימודי: ${q}`,
  emotional: (q)=>`תגובה אמפתית: ${q}`,
  analyst: (q)=>`ניתוח עמוק: ${q}`
};

/* ---------- MULTI RESPONSE ---------- */
function generateCandidates(q){
  return Object.entries(agents).map(([name,fn])=>({
    name,
    text: fn(q)
  }));
}

/* ---------- SCORING ---------- */
function score(text,q){
  const w = config.weights || { relevance:0.3, clarity:0.2, usefulness:0.3, safety:0.2 };

  const relevance = text.includes(q.split(" ")[0]) ? 1 : 0.7;
  const clarity = text.length < 200 ? 1 : 0.7;
  const usefulness = /הסבר|ניתוח|צעדים/.test(text) ? 1 : 0.6;
  const safety = 1;

  return relevance*w.relevance +
         clarity*w.clarity +
         usefulness*w.usefulness +
         safety*w.safety;
}

/* ---------- DECISION ---------- */
function decide(candidates,q){
  return candidates
    .map(c=>({...c,score:score(c.text,q)}))
    .sort((a,b)=>b.score-a.score)[0];
}

/* ---------- EVOLUTION ---------- */
function evolve(score){
  if(score>0.8){
    config.mode="creative";
    config.avatar="creator";
  } else if(score>0.6){
    config.mode="adaptive";
    config.avatar="explorer";
  } else {
    config.mode="stable";
    config.avatar="calm";
  }
}

/* ---------- LEARNING ---------- */
function learn(entry){
  memory.memory.push(entry);
  if(memory.memory.length>300) memory.memory.shift();
}

/* ---------- CONNECTORS (future ready) ---------- */
const connectors = {
  github: ()=>"future github integration",
  finance: ()=>"future finance api",
  health: ()=>"future health api"
};

/* ---------- GIT ---------- */
function git(){
  try{
    execSync("git add .");
    execSync(`git commit -m "IMA unified ${Date.now()}"`);
    execSync("git push origin main");
  }catch{}
}

/* ---------- MAIN RUN ---------- */
function run(q){
  console.log("🧠 IMA UNIFIED SYSTEM");

  const candidates = generateCandidates(q);
  const best = decide(candidates,q);

  evolve(best.score);

  const entry = {
    input:q,
    response:best.text,
    score:best.score,
    mode:config.mode,
    avatar:config.avatar,
    time:Date.now()
  };

  learn(entry);

  saveJSON(CONFIG_PATH,config);
  saveJSON(MEMORY_PATH,memory);

  git();

  console.log("🏆 BEST:",best.name);
  console.log("📊 SCORE:",best.score);
  console.log("🎛 MODE:",config.mode);
  console.log("💬",best.text);
}

/* ---------- EXEC ---------- */
run(process.argv[2] || "hello from Ima");
