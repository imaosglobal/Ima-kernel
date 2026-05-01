
const { execSync } = require("child_process");
const memory = require("./brain_memory");

function state() {
  try {
    const health = JSON.parse(execSync("curl -s http://localhost:4000/health"));
    const queue = JSON.parse(execSync("curl -s http://localhost:4000/v2/queue"));
    return { health, queue };
  } catch (e) {
    return { error: e.message };
  }
}

function risk(history) {

  const restarts = history.filter(x => x.decision?.action === "restart").length;

  const failures = history.filter(x => x.state?.error).length;

  return restarts * 2 + failures * 3;
}

function decide(s, history) {

  const r = risk(history);

  // 🧠 אם יש יותר מדי restartים → נעילה זמנית
  if (r > 6) {
    return {
      action: "stable",
      reason: "risk_lock: too many failures",
      risk: r
    };
  }

  if (s.error) {
    return { action: "restart", reason: "system error", risk: r };
  }

  if (!s.health?.ok) {
    return { action: "restart", reason: "unhealthy", risk: r };
  }

  return { action: "stable", reason: "ok", risk: r };
}

(function main() {

  const history = memory.last(30);
  const s = state();
  const d = decide(s, history);

  memory.save({ state: s, decision: d });

  console.log(JSON.stringify({
    state: s,
    decision: d,
    risk: d.risk,
    history_size: history.length
  }, null, 2));

})();

