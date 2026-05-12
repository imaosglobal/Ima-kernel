const fs = require("fs");

function read(path, fallback) {
  try {
    return JSON.parse(fs.readFileSync(path, "utf-8"));
  } catch {
    return fallback;
  }
}

function decideProductDirection() {
  const memory = read("ima_memory.json", []);

  const tasks = memory.filter(m => m.type === "request");

  const patterns = {};

  for (const t of tasks) {
    const key = t.path || "unknown";
    patterns[key] = (patterns[key] || 0) + 1;
  }

  const sorted = Object.entries(patterns).sort((a,b)=>b[1]-a[1]);

  const top = sorted[0] || ["idle", 0];

  const decision = {
    focus: top[0],
    intensity: top[1],
    recommendation:
      top[1] > 10 ? "build_feature" :
      top[1] > 3 ? "improve_feature" :
      "observe"
  };

  const state = read("ima_state.json", {});
  state.product_brain = decision;

  fs.writeFileSync("ima_state.json", JSON.stringify(state, null, 2));

  return decision;
}

module.exports = { decideProductDirection };
