
const { execSync } = require("child_process");
const fs = require("fs");

const PID_FILE = process.env.HOME + "/ima_core/kernel/.daemon_pid";

function isAlive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

function getPid() {
  try {
    return parseInt(fs.readFileSync(PID_FILE));
  } catch {
    return null;
  }
}

function restart() {
  console.log("[WATCHDOG] restarting daemon...");
  execSync("bash ~/ima_core/kernel/start_daemon.sh");
}

setInterval(() => {
  const pid = getPid();
  if (!pid || !isAlive(pid)) {
    restart();
  }
}, 5000);

console.log("[WATCHDOG] running...");

