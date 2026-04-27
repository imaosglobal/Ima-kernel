const fs = require("fs");
const { execSync } = require("child_process");

function listGit() {
  try {
    const repos = execSync("git remote -v").toString();
    const status = execSync("git status").toString();
    const log = execSync("git log -1 --oneline").toString();

    return {
      timestamp: Date.now(),
      repos,
      status,
      last_commit: log
    };
  } catch (e) {
    return { error: e.message };
  }
}

function generateMap() {
  const map = {
    system: "IMA_FULL_SYSTEM_MAP",
    core_modules: [
      "kernel",
      "runtime",
      "brain",
      "behavior",
      "evolution",
      "extension",
      "orchestrator"
    ],
    snapshot: listGit()
  };

  fs.writeFileSync(
    "./ima_system_map.json",
    JSON.stringify(map, null, 2)
  );

  console.log("🗺 SYSTEM MAP GENERATED");

  return map;
}

function decideAction(map) {
  const score = Math.random() * 100; // placeholder for real intelligence

  let action = "maintain";

  if (score > 70) action = "expand";
  else if (score < 40) action = "stabilize";

  console.log("🧠 SYSTEM DECISION:", action);

  fs.writeFileSync(
    "./ima_system_decision.json",
    JSON.stringify({ action, score, time: Date.now() }, null, 2)
  );
}

const map = generateMap();
decideAction(map);
