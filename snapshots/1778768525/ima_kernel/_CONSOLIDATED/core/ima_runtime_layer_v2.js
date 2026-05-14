const fs = require("fs");
const path = require("path");
const cp = require("child_process");

const ROOT = process.env.HOME + "/ima_workspace";
const STATE = path.join(ROOT, "core/state.json");
const LOCK = path.join(ROOT, "runtime.lock");

fs.mkdirSync(path.join(ROOT, "core"), { recursive: true });
fs.mkdirSync(path.join(ROOT, "logs"), { recursive: true });

function exec(cmd) {
  try {
    return cp.execSync(cmd, {
      cwd: ROOT,
      shell: true,
      encoding: "utf8"
    }).toString().trim();
  } catch {
    return null;
  }
}

// ===============================
// SAFE LOCK
// ===============================
if (fs.existsSync(LOCK)) {
  const prev = JSON.parse(fs.readFileSync(LOCK));
  if (Date.now() - prev.ts < 5000) {
    console.log("ALREADY RUNNING");
    process.exit(0);
  }
}
fs.writeFileSync(LOCK, JSON.stringify({ ts: Date.now() }));

// ===============================
// RUNTIME DISCOVERY
// ===============================
function findRuntime() {
  const candidates = [
    "server.js",
    "runtime/server.js",
    "runtime/autonomous_runtime.js"
  ];

  return candidates.find(f => fs.existsSync(path.join(ROOT, f))) || null;
}

// ===============================
// HEARTBEAT
// ===============================
function heartbeat() {
  fs.writeFileSync(
    path.join(ROOT, "logs/heartbeat.json"),
    JSON.stringify({
      time: Date.now(),
      pid: process.pid
    }, null, 2)
  );
}

// ===============================
// DAEMON CONTROL (SINGLE SAFE MODE)
// ===============================
let runtime = findRuntime();

function startDaemon(file) {
  if (!file) return;

  exec(`pkill -f node || true`);

  const child = cp.spawn("node", [file], {
    cwd: ROOT,
    detached: true,
    stdio: "ignore"
  });

  child.unref();

  console.log("DAEMON STARTED:", file);
  return child.pid;
}

// start once
startDaemon(runtime);

// ===============================
// MAIN LOOP
// ===============================
setInterval(() => {
  heartbeat();

  const newRuntime = findRuntime();

  if (newRuntime && newRuntime !== runtime) {
    console.log("RUNTIME SWITCH");
    runtime = newRuntime;
    startDaemon(runtime);
  }

  fs.writeFileSync(
    STATE,
    JSON.stringify({
      runtime,
      ts: Date.now()
    }, null, 2)
  );

}, 4000);

console.log("IMA RUNTIME V2 ACTIVE");
