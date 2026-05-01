
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

function decide(s, history) {

  // כלל למידה פשוט: אם היו הרבה restartים לאחרונה → להימנע
  const recentRestarts = history
    .slice(-10)
    .filter(x => x.decision?.action === "restart").length;

  if (recentRestarts > 3) {
    return { action: "stable", reason: "learning: too many restarts" };
  }

  if (s.error) return { action: "restart", reason: "system down" };
  if (!s.health?.ok) return { action: "restart", reason: "unhealthy" };

  return { action: "stable", reason: "ok" };
}

(function main() {

  const history = memory.getAll();
  const s = state();
  const d = decide(s, history);

  memory.save({
    state: s,
    decision: d
  });

  console.log(JSON.stringify({
    state: s,
    decision: d,
    memory_size: history.length
  }, null, 2));

})();

