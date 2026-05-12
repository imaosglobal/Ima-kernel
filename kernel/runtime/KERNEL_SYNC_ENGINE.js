const fs = require("fs");
const { execSync } = require("child_process");

function sh(cmd) {
  try {
    return execSync(cmd).toString().trim();
  } catch {
    return null;
  }
}

function getLocalVersion() {
  const pkg = JSON.parse(fs.readFileSync("package.json", "utf8"));
  return pkg.version;
}

function getGitVersion() {
  const tag = sh("git describe --tags --abbrev=0");
  return tag ? tag.replace("v", "") : null;
}

function getNpmVersion(pkgName) {
  const v = sh(`npm view ${pkgName} version`);
  return v;
}

function syncPlan() {
  const pkg = JSON.parse(fs.readFileSync("package.json", "utf8"));
  const name = pkg.name;

  const local = getLocalVersion();
  const git = getGitVersion();
  const npm = getNpmVersion(name);

  return {
    local,
    git,
    npm,
    drift: {
      gitMismatch: git !== local,
      npmMismatch: npm !== local
    }
  };
}

function printPlan() {
  const p = syncPlan();
  console.log("=== SYNC STATE ===");
  console.log(JSON.stringify(p, null, 2));
  return p;
}

module.exports = { printPlan, syncPlan };
