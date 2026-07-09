const fs = require('fs');
const { execSync } = require('child_process');

const STATE_FILE = './runtime/kernel_state.json';

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return { runtime: "booting", lastHeartbeat: 0, status: "booting" };
  }
}

function saveState(s) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(s, null, 2));
}

function runCI() {
  try {
    execSync("node runtime/enforce_fs_controller.js", { stdio: "inherit" });
    return true;
  } catch {
    return false;
  }
}

function evaluate() {
  const s = loadState();

  const healthy =
    s.runtime === "alive" &&
    Date.now() - (s.lastHeartbeat || 0) < 10000;

  return healthy;
}

function promote() {
  const pkg = JSON.parse(fs.readFileSync("package.json", "utf8"));

  const parts = pkg.version.split(".").map(Number);
  parts[2] += 1;
  pkg.version = parts.join(".");

  fs.writeFileSync("package.json", JSON.stringify(pkg, null, 2));
  return pkg.version;
}

function rollback() {
  console.log("ROLLBACK: restoring previous state");
  execSync("git checkout -- runtime", { stdio: "inherit" });
}

function loop() {
  console.log("=== KERNEL LOOP START ===");

  const ci = runCI();
  if (!ci) return rollback();

  const ok = evaluate();
  if (!ok) return rollback();

  const v = promote();
  console.log("PROMOTED VERSION:", v);

  const state = loadState();
  state.status = "released";
  state.version = v;
  saveState(state);

  console.log("=== LOOP COMPLETE ===");
}

loop();
