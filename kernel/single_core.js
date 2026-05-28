const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const LOCK = path.join(ROOT, "runtime", "ima.lock");
const SERVER = path.join(ROOT, "server.js");

function isAlive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

function acquireLock() {
  try {
    if (fs.existsSync(LOCK)) {
      const pid = parseInt(fs.readFileSync(LOCK, "utf8"));
      if (pid && isAlive(pid)) {
        return null; // כבר רץ
      }
    }
  } catch {}

  fs.writeFileSync(LOCK, process.pid.toString());
  return true;
}

function startServerOnce() {
  if (!acquireLock()) {
    process.exit(0);
  }

  const child = spawn("node", [SERVER], {
    detached: true,
    stdio: "ignore"
  });

  child.unref();

  console.log("[IMA] SINGLE CORE STARTED PID:", child.pid);
}

startServerOnce();
