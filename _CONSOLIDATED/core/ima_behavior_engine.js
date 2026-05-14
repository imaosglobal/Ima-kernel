const fs = require("fs");

const STATE_FILE = "./ima_evolution_state.json";
const PROFILE_FILE = "./ima_behavior_profile.json";

function load(file) {
  return JSON.parse(fs.readFileSync(file));
}

function save(file, data) {
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
}

function updateBehavior() {
  const state = load(STATE_FILE);
  const profile = load(PROFILE_FILE);

  const avg = state.score_history?.length
    ? state.score_history.reduce((a,b)=>a+b,0)/state.score_history.length
    : 50;

  console.log("📊 BEHAVIOR INPUT AVG:", avg.toFixed(2));

  // 🧠 התאמות בזמן אמת (זה הלב של השלב)

  if (avg > 55) {
    profile.creativity += 0.1;
    profile.verbosity += 0.1;
    profile.tone = "expansive";
  }

  if (avg < 45) {
    profile.creativity -= 0.1;
    profile.verbosity -= 0.1;
    profile.tone = "minimal";
  }

  // גבולות בטיחות
  profile.creativity = Math.max(0.1, Math.min(1, profile.creativity));
  profile.verbosity = Math.max(0.1, Math.min(1, profile.verbosity));

  save(PROFILE_FILE, profile);

  console.log("🧠 UPDATED PROFILE:", profile);
}

updateBehavior();
