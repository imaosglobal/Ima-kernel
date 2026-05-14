const fs = require("fs");

/* ---------- IO ---------- */
const CONFIG = "./ima_config.json";
const MEMORY = "./memory.json";

function load(p, fb){ try { return JSON.parse(fs.readFileSync(p)); } catch { return fb; } }
function save(p, d){ fs.writeFileSync(p, JSON.stringify(d,null,2)); }

let config = load(CONFIG, {
  mode: "adaptive",
  learning_mode: "multi",
});

let memory = load(MEMORY, { memory: [] });

/* ---------- LEARNING MODES ---------- */
const learners = {
  shallow: (q)=>`תשובה מהירה: ${q}`,
  deep: (q)=>`ניתוח עמוק: ${q} → פירוק, קשרים, השלכות`,
  very_deep: (q)=>`ניתוח רב-שכבתי: ${q} → פסיכולוגי, חברתי, לוגי`,
  humor: (q)=>`תשובה עם קלילות: ${q} 😄`,
};

/* ---------- MULTI LEARNING ---------- */
function learnAll(q){
  return Object.entries(learners).map(([type,fn])=>({
    type,
    text: fn(q)
  }));
}

/* ---------- SCORING ---------- */
function score(x){
  let base = x.text.length / 100;
  if(x.type==="very_deep") base += 0.3;
  if(x.type==="deep") base += 0.2;
  if(x.type==="humor") base += 0.1;
  return Math.min(1, base);
}

/* ---------- DECISION ---------- */
function decide(list){
  return list
    .map(x=>({...x,score:score(x)}))
    .sort((a,b)=>b.score-a.score)[0];
}

/* ---------- ADAPT ---------- */
function adapt(best){
  if(best.type==="very_deep"){
    config.mode="analysis";
  } else if(best.type==="deep"){
    config.mode="thinking";
  } else if(best.type==="humor"){
    config.mode="social";
  } else {
    config.mode="fast";
  }
}

/* ---------- MEMORY ---------- */
function store(entry){
  memory.memory.push(entry);
  if(memory.memory.length>200) memory.memory.shift();
}

/* ---------- RUN ---------- */
function run(q){
  console.log("🧠 IMA DEEP LEARNING ENGINE");

  const variants = learnAll(q);
  const best = decide(variants);

  adapt(best);

  const entry = {
    input:q,
    best:best.text,
    type:best.type,
    score:best.score,
    mode:config.mode,
    time:Date.now()
  };

  store(entry);
  save(CONFIG,config);
  save(MEMORY,memory);

  console.log("🏆 TYPE:",best.type);
  console.log("📊 SCORE:",best.score);
  console.log("🎛 MODE:",config.mode);
  console.log("💬",best.text);
}

/* ---------- EXEC ---------- */
run(process.argv[2] || "מה זה למידה?");
