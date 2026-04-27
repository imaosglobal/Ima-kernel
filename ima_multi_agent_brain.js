const fs = require("fs");

/* ---------- SAFE LOAD ---------- */
function load(p, fb){
  try { return JSON.parse(fs.readFileSync(p)); }
  catch { return fb; }
}

function save(p, d){
  fs.writeFileSync(p, JSON.stringify(d,null,2));
}

/* ---------- MEMORY ---------- */
const MEMORY_FILE = "./ima_memory.json";

let memory = load(MEMORY_FILE, { events: [] });
if(!memory.events) memory.events = [];

/* ---------- AGENTS ---------- */
const agents = [
  {
    name: "logic",
    respond: (e)=>({
      text: `LOGIC: analyze ${e.type}`,
      score: 0.8
    })
  },
  {
    name: "creative",
    respond: (e)=>({
      text: `CREATIVE: reinterpret ${e.type}`,
      score: 0.6 + Math.random()*0.4
    })
  },
  {
    name: "stable",
    respond: (e)=>({
      text: `STABLE: safe processing ${e.type}`,
      score: 0.9
    })
  }
];

/* ---------- CONSENSUS ---------- */
function consensus(results){
  let best = results[0];

  for(const r of results){
    if(r.score > best.score){
      best = r;
    }
  }

  return best;
}

/* ---------- EVENT PROCESS ---------- */
function processEvent(event){
  const results = agents.map(a => a.respond(event));

  const winner = consensus(results);

  memory.events.push({
    event,
    results,
    winner,
    time: Date.now()
  });

  if(memory.events.length > 300){
    memory.events.shift();
  }

  save(MEMORY_FILE, memory);

  return { results, winner };
}

/* ---------- LOOP ---------- */
setInterval(()=>{
  const event = { type: "tick", time: Date.now() };

  const out = processEvent(event);

  console.log("📡 EVENT:", event.type);
  console.log("🏆 WINNER:", out.winner.text);
}, 2000);

console.log("🧠 IMA MULTI-AGENT BRAIN STARTED");
