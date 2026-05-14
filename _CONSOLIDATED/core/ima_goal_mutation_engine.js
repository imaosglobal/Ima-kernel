const fs = require("fs");

const GOAL_FILE = "goals.json";

function loadGoals() {
  if (!fs.existsSync(GOAL_FILE)) {
    return {
      maxResponseMs: 30,
      allowError: false,
      memoryGrowthLimit: 50
    };
  }
  return JSON.parse(fs.readFileSync(GOAL_FILE));
}

function saveGoals(goals) {
  fs.writeFileSync(GOAL_FILE, JSON.stringify(goals, null, 2));
}

// התאמת מטרות לפי מציאות
function mutateGoals(metrics) {
  let goals = loadGoals();

  console.log("🧠 GOAL MUTATION CHECK");

  // אם המערכת תמיד איטית → מרפים יעד
  if (metrics.avgResponse > goals.maxResponseMs * 1.5) {
    goals.maxResponseMs = Math.min(goals.maxResponseMs + 5, 200);
    console.log("📉 relaxing latency goal");
  }

  // אם הכל מהיר → מחמירים יעד
  if (metrics.avgResponse < goals.maxResponseMs * 0.5) {
    goals.maxResponseMs = Math.max(goals.maxResponseMs - 2, 10);
    console.log("📈 tightening latency goal");
  }

  saveGoals(goals);

  return goals;
}

module.exports = { mutateGoals, loadGoals };
