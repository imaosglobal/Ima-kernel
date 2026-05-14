const fs = require("fs");
const { execSync } = require("child_process");

function load(file) {
  try {
    return JSON.parse(fs.readFileSync(file));
  } catch {
    return null;
  }
}

function run() {
  const decision = load("./ima_system_decision.json");
  const map = load("./ima_system_map.json");

  if (!decision) {
    console.log("⚠️ NO DECISION FOUND");
    return;
  }

  console.log("🧠 EXECUTION MODE:", decision.action);

  try {
    // 1. STABILIZE → רק commit נקי
    if (decision.action === "stabilize") {
      execSync("git add -A");
      execSync(`git commit -m "auto stabilize ${Date.now()}"`);
      execSync("git push");
      console.log("📦 STABILIZATION COMMITTED");
    }

    // 2. EXPAND → יצירת מודול חדש
    if (decision.action === "expand") {
      const name = `auto_exec_${Date.now()}.js`;

      const code = `
module.exports = {
  type: "auto-generated",
  created: ${Date.now()},
  behavior: "expansion module",
  run: () => "IMA expansion executed"
};
`;

      fs.writeFileSync(`./ima_runtime/${name}`, code);

      execSync("git add -A");
      execSync(`git commit -m "auto expand ${name}"`);
      execSync("git push");

      console.log("🚀 EXPANSION EXECUTED:", name);
    }

    // 3. MAINTAIN → רק log
    if (decision.action === "maintain") {
      console.log("🧠 NO ACTION REQUIRED - SYSTEM STABLE");
    }

  } catch (e) {
    console.log("❌ EXECUTION ERROR:", e.message);
  }
}

run();
