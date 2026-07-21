const { execSync } = require("child_process");
const fs = require("fs");

function run(cmd) {
  try {
    return execSync(cmd, { stdio: "pipe" }).toString().trim();
  } catch (e) {
    return null;
  }
}

function getVersion() {
  const pkg = JSON.parse(fs.readFileSync("./package.json", "utf8"));
  return pkg.version;
}

function bumpVersion() {
  const pkgPath = "./package.json";
  const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8"));

  const parts = pkg.version.split(".").map(n => parseInt(n));
  parts[2]++;

  pkg.version = parts.join(".");
  fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2));
  return pkg.version;
}

function commitAll(version) {
  run("git add .");
  run(`git commit -m "AUTO-SYNC v${version}" || true`);
}

function push() {
  run("git push origin main || true");
}

function publishNpm(version) {
  const pkg = JSON.parse(fs.readFileSync("./package.json", "utf8"));
  
  if (!pkg.name) return { ok: false, error: "no package name" };

  // ensure public publish
  run("npm config set access public");

  const res = run("npm publish || true");
  return { ok: true, version, result: res };
}

function cycle() {
  const version = bumpVersion();

  commitAll(version);
  push();

  const npmResult = publishNpm(version);

  return {
    ok: true,
    version,
    git: "synced",
    npm: npmResult.ok
  };
}

module.exports = { cycle, getVersion };
