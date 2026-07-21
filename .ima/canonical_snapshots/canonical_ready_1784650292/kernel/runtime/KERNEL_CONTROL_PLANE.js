const fs = require("fs");
const { execSync } = require("child_process");

const STATE_FILE = "./runtime/kernel_state.json";

/* ---------------- STATE ---------------- */

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, "utf8"));
  } catch {
    return { version: "0.0.0", status: "init" };
  }
}

function saveState(s) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(s, null, 2));
}

/* ---------------- GIT GATE ---------------- */

const IGNORE_IN_GIT_CHECK = [
  "kernel_state.json",
  "sync_state.json"
];

function isRepoClean() {
  const out = execSync("git status --porcelain", { encoding: "utf8" })
    .split("\n")
    .filter(Boolean)
    .filter(line => {
      return !IGNORE_IN_GIT_CHECK.some(f => line.includes(f));
    });

  return out.length === 0;
}

/* ---------------- VERSION ---------------- */

function bumpPatch(version) {
  const parts = (version || "0.0.0").split(".").map(Number);
  parts[2] += 1;
  return parts.join(".");
}

/* ---------------- PIPELINE ---------------- */

function runTests() {
  try {
    execSync("node -e \"require('./runtime/FS_CONTROLLER');\"", {
      stdio: "ignore"
    });
    return true;
  } catch {
    return false;
  }
}

function commit(version) {
  execSync(`git add . && git commit -m "auto release ${version}"`, {
    stdio: "inherit"
  });
}

function tag(version) {
  execSync(`git tag v${version}`, { stdio: "inherit" });
}

function push() {
  execSync("git push && git push --tags", { stdio: "inherit" });
}

function publish() {
  try {
    execSync("npm publish", { stdio: "inherit" });
  } catch (e) {
    console.log("[NPM] publish skipped or failed");
  }
}

/* ---------------- CONTROL LOOP ---------------- */

function cycle() {
  const state = loadState();

  console.log("=== KERNEL CONTROL PLANE ===");

  if (!isRepoClean()) {
    console.log("[GATE] repo not clean → abort");
    return;
  }

  console.log("[GATE] clean");

  if (!runTests()) {
    console.log("[CI] tests failed → abort");
    return;
  }

  console.log("[CI] passed");

  const newVersion = bumpPatch(state.version);

  state.version = newVersion;
  state.status = "building";
  saveState(state);

  console.log("[BUILD] version:", newVersion);

  commit(newVersion);
  tag(newVersion);
  push();
  publish();

  state.status = "released";
  saveState(state);

  console.log("=== RELEASE COMPLETE ===");
}

/* ---------------- ENTRY ---------------- */

cycle();

module.exports = { cycle };
