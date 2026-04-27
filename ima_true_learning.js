const fs = require("fs");

/* ---------- STORAGE ---------- */
const FILE = "./ima_learning_state.json";

function load(p, fb){
  try { return JSON.parse(fs.readFileSync(p)); }
  catch { return fb; }
}

function save(p, d){
  fs.writeFileSync(p, JSON.stringify(d,null,2));
}

/* ---------- STATE ---------- */
let state = load(FILE, {
  data: [],
  weights: {
    logic: 1.0,
    creative: 1.0,
    stable: 1.0
  }
});

/* ---------- AGENTS ---------- */
const agents = {
  logic: (e)=>({ answer:`logic:${e.type}`, score: 0.7 }),
  creative: (e)=>({ answer:`creative:${e.type}`, score: 0.6 + Math.random()*0.4 }),
  stable: (e)=>({ answer:`stable:${e.type}`, score: 0.9 })
};

/* ---------- PICK ---------- */
function choose(results){
  let best = results[0];

  for(const r of results){
    if(r.score > best.score){
      best = r;
    }
  }

  return best;
}

/* ---------- LEARN ---------- */
function updateWeights(winnerName, score){
  if(score > 0.8){
    state.weights[winnerName] += 0.05;
  } else {
    state.weights[winnerName] -= 0.02;
  }

  // clamp
  for(const k in state.weights){
    state.weights[k] = Math.max(0.1, Math.min(2.0, state.weights[k]));
  }
}

/* ---------- PROCESS ---------- */
function process(event){
  const results = Object.keys(agents).map(name=>{
    const r = agents[name](event);

    // apply weight
    r.score *= state.weights[name];

    r.name = name;
    return r;
  });

  const winner = choose(results);

  updateWeights(winner.name, winner.score);

  state.data.push({
    event,
    results,
    winner,
    weights: {...state.weights},
    time: Date.now()
  });

  if(state.data.length > 300){
    state.data.shift();
  }

  save(FILE, state);

  return winner;
}

/* ---------- LOOP ---------- */
setInterval(()=>{
  const event = { type: "tick", time: Date.now() };

  const result = process(event);

  console.log("📡 EVENT:", event.type);
  console.log("🏆 WINNER:", result.answer);
  console.log("⚖️ WEIGHTS:", state.weights);
}, 2000);

console.log("🧠 IMA TRUE LEARNING SYSTEM STARTED");
