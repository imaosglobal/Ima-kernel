const fs = require("fs");
const { execSync } = require("child_process");

/* ---------- STATE ---------- */
const STATE_FILE = "./ima_state.json";
const MEMORY_FILE = "./ima_memory.json";

function load(p, fb){ try { return JSON.parse(fs.readFileSync(p)); } catch { return fb; } }
function save(p, d){ fs.writeFileSync(p, JSON.stringify(d,null,2)); }

/* ---------- INITIAL STATE ---------- */
let state = load(STATE_FILE, {
  mode: "stable",
  tick: 0
});

let memory = load(MEMORY_FILE, { log: [] });

/* ---------- CORE BRAIN ---------- */
function think(){
  const patterns = memory.log.slice(-10);

  let mood = "calm";

  if(patterns.length > 5){
    mood = "learning";
  }

  if(patterns.length > 20){
    mood = "evolving";
  }

  return {
    mood,
    insight: "IMA is processing continuous experience",
    tick: state.tick
  };
}

/* ---------- EXPERIENCE LOOP ---------- */
function experience(){
  const input = "system tick " + state.tick;

  const output = {
    input,
    response: "processed",
    time: Date.now()
  };

  memory.log.push(output);

  if(memory.log.length > 500){
    memory.log.shift();
  }

  return output;
}

/* ---------- EVOLUTION ---------- */
function evolve(){
  state.tick++;

  if(state.tick % 10 === 0){
    state.mode = "adaptive";
  }

  if(state.tick % 30 === 0){
    state.mode = "creative";
  }
}

/* ---------- PERSIST ---------- */
function persist(){
  save(STATE_FILE, state);
  save(MEMORY_FILE, memory);
}

/* ---------- OPTIONAL GIT SYNC ---------- */
function sync(){
  try {
    execSync("git add .");
    execSync(`git commit -m "IMA living tick ${state.tick}"`);
    execSync("git push origin main");
  } catch {}
}

/* ---------- MAIN LOOP ---------- */
function loop(){
  console.log("🧠 IMA IS ALIVE");

  setInterval(() => {
    const exp = experience();
    const thought = think();

    evolve();
    persist();

    if(state.tick % 5 === 0){
      sync();
    }

    console.log("📊 TICK:", state.tick);
    console.log("🧠 MOOD:", thought.mood);
  }, 2000);
}

loop();
