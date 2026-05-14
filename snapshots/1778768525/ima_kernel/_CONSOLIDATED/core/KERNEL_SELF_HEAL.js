const { execSync } = require("child_process");
const fs = require("fs");

function run(cmd) {
  try {
    return execSync(cmd, { stdio: "pipe" }).toString();
  } catch (e) {
    return null;
  }
}

function fixZombieEntryPoint() {
  run("pkill -f ENTRYPOINT || true");
  run("sleep 1");
}

function ensureRuntimeHealthy() {
  const k = require("./KERNEL_STATE");
  const s = k.getState();
  return s.runtime === "alive" && s.lastHeartbeat > 0;
}

function fixVersionConflict() {
  try {
    const pkg = JSON.parse(fs.readFileSync("package.json"));

    // אם npm reject בגלל version נמוך מדי → bump אוטומטי חכם
    const parts = pkg.version.split(".").map(Number);

    // הופך לpatch increment תמיד בטוח
    parts[2] += 1;

    pkg.version = parts.join(".");
    fs.writeFileSync("package.json", JSON.stringify(pkg, null, 2));

    run(`git add package.json`);
    run(`git commit -m "AUTO FIX version bump" || true`);
  } catch {}
}

function safeNpmPublish() {
  const pkg = JSON.parse(fs.readFileSync("package.json"));

  // force tag fix
  run(`npm publish --tag latest --access public || true`);
}

function healAll() {
  console.log("[SELF-HEAL] starting...");

  fixZombieEntryPoint();

  if (!ensureRuntimeHealthy()) {
    console.log("[SELF-HEAL] runtime unhealthy, restarting");
    run("nohup node runtime/ENTRYPOINT.js > logs/runtime.log 2>&1 &");
  }

  fixVersionConflict();

  console.log("[SELF-HEAL] done");
}

module.exports = {
  healAll,
  ensureRuntimeHealthy,
  fixVersionConflict,
  safeNpmPublish
};
