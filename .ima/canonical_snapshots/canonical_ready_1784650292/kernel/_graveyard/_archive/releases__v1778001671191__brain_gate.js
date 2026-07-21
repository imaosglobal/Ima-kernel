
const { execSync } = require("child_process");

function brain() {
  return JSON.parse(
    execSync("node ~/ima_core/kernel/control_brain.js").toString()
  );
}

function allow(action) {
  const b = brain();

  if (action === "restart" && b.decision.action === "restart") {
    return true;
  }

  if (b.decision.action === "stable") {
    return true;
  }

  return false;
}

module.exports = { allow };

