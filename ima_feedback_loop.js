const fs = require("fs");
const { execSync } = require("child_process");

function load(file) {
  try {
    return JSON.parse(fs.readFileSync(file));
  } catch {
    return null;
  }
}

function getGitScore() {
  try {
    const log = execSync("git log -1 --oneline").toString();
    const diff = execSync("git diff --shortstat").toString();

    // proxy פשוט לאיכות שינוי
    const score = log.length + diff.length;
    return score;
  } catch {
    return 50;
  }
}

function updateLearning() {
  const decision = load("./ima_system_decision.json") || {};
  const historyFile = "./ima_learning_loop.json";

  const score = getGitScore();

  let history = [];
  try {
    history = JSON.parse(fs.readFileSync(historyFile));
  } catch {}

  history.push({
    time: Date.now(),
    score,
    action: decision.action || "unknown"
  });

  // שמירה של מקסימום 20 רשומות
  if (history.length > 20) history.shift();

  fs.writeFileSync(historyFile, JSON.stringify(history, null, 2));

  console.log("🧠 FEEDBACK UPDATED:", {
    latestScore: score,
    action: decision.action
  });

  // התאמת סף דינמית
  const avg = history.reduce((a,b)=>a + (b.score||0),0) / history.length;

  let newThreshold = 52;

  if (avg > 80) newThreshold = 48;
  if (avg < 40) newThreshold = 55;

  fs.writeFileSync(
    "./ima_dynamic_threshold.json",
    JSON.stringify({ threshold: newThreshold, avg }, null, 2)
  );

  console.log("⚙️ NEW THRESHOLD:", newThreshold);
}

updateLearning();
