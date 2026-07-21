const fs = require("fs");
const cp = require("child_process");

function exec(cmd) {
  try {
    return cp.execSync(cmd, {
      shell: "/bin/bash",
      encoding: "utf8",
      stdio: "pipe"
    }).trim();
  } catch {
    return null;
  }
}

console.log("=== IMA SAFE RELOAD ===");

if (!fs.existsSync("logs")) {
  fs.mkdirSync("logs", { recursive: true });
}

const daemon = "server.js";

console.log("CHECK NODE SYNTAX...");
const syntax = exec(`node --check ${daemon}`);

if (syntax === null) {
  console.log("SYNTAX ERROR IN:", daemon);
  process.exit(1);
}

console.log("RESTARTING DAEMON...");
exec(`pkill -f "node ${daemon}" || true`);

exec(`nohup node ${daemon} > logs/server.log 2>&1 &`);

setTimeout(() => {
  const running = exec(`pgrep -f "node ${daemon}"`);

  fs.writeFileSync(
    "logs/reload_state.json",
    JSON.stringify({
      daemon,
      running: !!running,
      time: Date.now()
    }, null, 2)
  );

  console.log("RUNNING:", !!running);
  console.log("=== DONE ===");
}, 2000);
