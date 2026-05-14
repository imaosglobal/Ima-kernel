const fs = require("fs");
const { execSync } = require("child_process");

/* ---------- SAFE LOAD ---------- */
function load(p, fb){
  try { return JSON.parse(fs.readFileSync(p)); }
  catch { return fb; }
}

function save(p, d){
  fs.writeFileSync(p, JSON.stringify(d,null,2));
}

/* ---------- STATE ---------- */
const STATE_FILE = "./ima_runtime_state.json";

let state = load(STATE_FILE, {
  modules: [],
  lastRun: 0,
  mode: "stable"
});

/* ---------- MODULE LOADER ---------- */
function loadModule(path){
  try {
    const mod = require(path);
    if(mod && mod.name){
      state.modules.push(mod.name);
      return mod;
    }
  } catch (e) {
    console.log("⚠ module failed:", path);
  }
  return null;
}

/* ---------- CORE ENGINE ---------- */
function runEngine(input){
  let result = `CORE: ${input}`;

  if(state.modules.length > 0){
    result += ` | modules: ${state.modules.join(",")}`;
  }

  return result;
}

/* ---------- EVOLUTION ---------- */
function evolve(){
  const count = state.modules.length;

  if(count > 2) state.mode = "adaptive";
  if(count > 5) state.mode = "creative";
}

/* ---------- SAFE GIT ---------- */
function gitSync(){
  try {
    execSync("git add .");

    const status = execSync("git status --porcelain").toString();

    if(status.trim().length > 0){
      execSync(`git commit -m "IMA runtime update ${Date.now()}"`);
      execSync("git push origin main");
      console.log("🚀 Git synced");
    }
  } catch (e) {
    console.log("⚠ Git skipped");
  }
}

/* ---------- BOOT ---------- */
function boot(input){
  console.log("🧠 IMA RUNTIME CORE STARTED");

  // load optional modules if exist
  loadModule("./ima_world_learning.js");
  loadModule("./ima_event_brain.js");

  evolve();

  const output = runEngine(input);

  state.lastRun = Date.now();

  save(STATE_FILE, state);
  gitSync();

  console.log("📊 MODE:", state.mode);
  console.log("💬 OUTPUT:", output);
}

/* ---------- EXEC ---------- */
const input = (process.argv && process.argv.slice(2).join(" ")) || "test run";

boot(input);
