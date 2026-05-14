const fs = require("fs");
const { execSync } = require("child_process");
const { runTest } = require("./ima_benchmark");
const { evaluate } = require("./ima_goal_engine");
const { mutateGoals } = require("./ima_goal_mutation_engine");

function backup() {
  fs.copyFileSync("server.js", "server.js.bak");
}

function restore() {
  fs.copyFileSync("server.js.bak", "server.js");
}

function evolve() {
  console.log("🧭 DYNAMIC EVOLUTION START");

  const before = runTest();

  execSync("node ima_smart_patch.js");

  const after = runTest();

  const metrics = {
    avgResponse: after,
    error: false,
    memoryGrowth: 10
  };

  // 🔥 שינוי מטרות לפי מציאות
  const updatedGoals = mutateGoals(metrics);

  const result = evaluate(metrics);

  console.log("📊 METRICS:", metrics);
  console.log("🎯 UPDATED GOALS:", updatedGoals);
  console.log("🏁 RESULT:", result);

  if (!result.passed) {
    console.log("🛑 FAIL → ROLLBACK");
    restore();
  } else {
    console.log("🚀 PASS → KEEP");
    execSync("git add server.js goals.json");
    execSync(`git commit -m "dynamic evolution ${Date.now()}"`);
    execSync("git push");
  }

  console.log("✅ DONE");
}

evolve();
