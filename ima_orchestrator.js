const fs = require("fs");
const { execSync } = require("child_process");

function load(file) {
  try {
    return JSON.parse(fs.readFileSync(file));
  } catch {
    return null;
  }
}

function score() {
  try {
    const out = execSync(
      "curl -s http://localhost:4000/ima/run -X POST -H 'Content-Type: application/json' -d '{\"message\":\"orchestrate\"}'"
    ).toString();
    const parsed = JSON.parse(out);
    return parsed.debug?.score || 50;
  } catch {
    return 50;
  }
}

function decide() {
  const state = load("./ima_evolution_state.json");
  const behavior = load("./ima_behavior_profile.json");

  const s = score();

  console.log("🧠 ORCHESTRATOR SCORE:", s);

  if (s > 55) {
    behavior.creativity = Math.min(1, behavior.creativity + 0.1);
    behavior.tone = "expansive";
  } else if (s < 45) {
    behavior.creativity = Math.max(0.1, behavior.creativity - 0.1);
    behavior.tone = "minimal";
  } else {
    behavior.tone = "stable";
  }

  fs.writeFileSync("./ima_behavior_profile.json", JSON.stringify(behavior, null, 2));

  console.log("🧠 UPDATED GLOBAL BEHAVIOR:", behavior);
}

decide();
