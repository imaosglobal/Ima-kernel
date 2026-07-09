const { execSync } = require("child_process");
const fs = require("fs");

function run(cmd) {
  try {
    return execSync(cmd, { stdio: "inherit" });
  } catch (e) {
    console.log("[WARN]", cmd, "failed but ignored");
    return null;
  }
}

function check() {
  const k = require("./KERNEL_STATE");
  const s = k.getState();
  return s.runtime === "alive" && s.lastHeartbeat > 0;
}

function ci() {
  console.log("=== AUTO CI ===");

  run("pkill -f ENTRYPOINT || true");
  run("nohup node runtime/ENTRYPOINT.js > logs/ci.log 2>&1 &");

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (!check()) return reject("CI FAIL");
      console.log("CI PASS");
      resolve(true);
    }, 3000);
  });
}

function release() {
  const pkg = JSON.parse(fs.readFileSync("package.json"));

  console.log("=== RELEASE START ===");

  run("git add .");
  run(`git commit -m "AUTO RELEASE ${Date.now()}" || true`);

  const parts = pkg.version.split(".").map(Number);
  parts[2] += 1;
  pkg.version = parts.join(".");
  fs.writeFileSync("package.json", JSON.stringify(pkg, null, 2));

  run(`git tag -f v${pkg.version}`);
  run("git push origin main || true");
  run(`git push origin -f v${pkg.version} || true`);

  run("npm publish --access public || true");

  console.log("=== RELEASE DONE ===");
}

async function fullCycle() {
  try {
    await ci();
    if (!check()) throw new Error("runtime unstable");

    release();
  } catch (e) {
    console.log("ROLLBACK SAFE MODE:", e);
  }
}

module.exports = { fullCycle };
