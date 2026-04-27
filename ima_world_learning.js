const fs = require("fs");

/* ---------- SAFE PROCESS FIX ---------- */
const args = (typeof process !== "undefined" && process.argv)
  ? process.argv.slice(2).join(" ")
  : "test query";

/* ---------- STORAGE ---------- */
const FILE = "./ima_world_state.json";

function load(p, fb){
  try { return JSON.parse(fs.readFileSync(p)); }
  catch { return fb; }
}

function save(p, d){
  fs.writeFileSync(p, JSON.stringify(d,null,2));
}

/* ---------- STATE ---------- */
let state = load(FILE, {
  memory: [],
  weights: { local: 1.0, world: 1.0 }
});

/* ---------- SIMULATED WORLD ---------- */
function fetchWorld(q){
  return {
    data: `world knowledge about: ${q}`,
    confidence: 0.7
  };
}

/* ---------- LOCAL ---------- */
function local(q){
  return {
    data: `local reasoning: ${q}`,
    confidence: 0.8
  };
}

/* ---------- DECISION ---------- */
function decide(localRes, worldRes){
  return (localRes.confidence >= worldRes.confidence)
    ? { source: "local", text: localRes.data }
    : { source: "world", text: worldRes.data };
}

/* ---------- LEARN ---------- */
function learn(winner){
  state.weights[winner.source] =
    (state.weights[winner.source] || 1) + 0.01;

  state.memory.push({
    winner,
    time: Date.now()
  });

  if(state.memory.length > 200){
    state.memory.shift();
  }

  save(FILE, state);
}

/* ---------- RUN ---------- */
const input = args || "test";

const l = local(input);
const w = fetchWorld(input);

const winner = decide(l, w);

learn(winner);

console.log("🌍 IMA WORLD LEARNING FIXED");
console.log("❓ INPUT:", input);
console.log("💬 ANSWER:", winner.text);
console.log("📡 SOURCE:", winner.source);
console.log("⚖️ WEIGHTS:", state.weights);
