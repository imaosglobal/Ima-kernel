const fs = require("fs");
const { execSync } = require("child_process");

/* ---------------- CONFIG ---------------- */
const CONFIG_PATH = "./ima_config.json";
const MEMORY_PATH = "./memory.json";

/* ---------------- LOAD/SAVE ---------------- */
function loadJSON(path, fallback) {
  try {
    return JSON.parse(fs.readFileSync(path));
  } catch {
    return fallback;
  }
}

function saveJSON(path, data) {
  fs.writeFileSync(path, JSON.stringify(data, null, 2));
}

/* ---------------- STATE ---------------- */
let config = loadJSON(CONFIG_PATH, {
  version: 1,
  mode: "local",
  evolution: true
});

let memory = loadJSON(MEMORY_PATH, { memory: [] });

/* ---------------- AI PROVIDER ---------------- */
function ask(input) {
  return `IMA LOCAL: ${input}`;
}

/* ---------------- SCORING ---------------- */
function scoreResponse(res) {
  return Math.min(100, res.length);
}

/* ---------------- EVOLUTION ---------------- */
function evolve(score) {
  if (!config.evolution) return;

  if (score > 80) {
    config.mode = "creative";
  } else if (score > 50) {
    config.mode = "adaptive";
  } else {
    config.mode = "stable";
  }
}

/* ---------------- GIT ---------------- */
function gitSync() {
  try {
    execSync("git add .");
    execSync(`git commit -m "IMA core update ${Date.now()}"`);
    execSync("git push origin main");
  } catch {}
}

/* ---------------- RUN ---------------- */
function run(input) {
  console.log("🧠 IMA CORE START");

  const response = ask(input);
  const score = scoreResponse(response);

  evolve(score);

  const entry = {
    input,
    response,
    score,
    mode: config.mode,
    time: Date.now()
  };

  memory.memory.push(entry);
  if (memory.memory.length > 200) memory.memory.shift();

  saveJSON(MEMORY_PATH, memory);
  saveJSON(CONFIG_PATH, config);

  gitSync();

  console.log("🧠 MODE:", config.mode);
  console.log("📊 SCORE:", score);
  console.log("💬 RESPONSE:", response);
}

/* ---------------- EXEC ---------------- */
run(process.argv[2] || "hello from IMA core");
