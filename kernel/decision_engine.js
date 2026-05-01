const fs = require("fs");

function read(path, fallback) {
  try {
    return JSON.parse(fs.readFileSync(path, "utf-8"));
  } catch {
    return fallback;
  }
}

function analyzeChanges() {
  const memory = read("ima_memory.json", []);

  const errorCount = memory.filter(e => e.type === "error").length;
  const reqCount = memory.filter(e => e.type === "request").length;

  const errorRate = reqCount ? errorCount / reqCount : 0;

  let decision = {
    shouldRelease: false,
    shouldPush: true,
    shouldRestart: false,
    reason: "ok"
  };

  if (errorRate > 0.1) {
    decision.shouldRestart = true;
    decision.reason = "instability detected";
  }

  if (errorRate < 0.01 && reqCount > 10) {
    decision.shouldRelease = true;
    decision.reason = "stable enough for release";
  }

  const state = read("ima_state.json", {});
  state.last_decision = decision;
  fs.writeFileSync("ima_state.json", JSON.stringify(state, null, 2));

  return decision;
}

module.exports = { analyzeChanges };
