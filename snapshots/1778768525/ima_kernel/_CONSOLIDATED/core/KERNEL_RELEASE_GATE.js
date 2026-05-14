const fs = require("fs");
const { execSync } = require("child_process");

const STATE_FILE = "./runtime/kernel_state.json";

function load() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, "utf8"));
  } catch {
    return null;
  }
}

function fail(msg) {
  console.log("[RELEASE GATE BLOCKED]", msg);
  process.exit(1);
}

// בדיקת יציבות לפני release
function validate() {
  const s = load();
  if (!s) fail("no state");

  if (!s.activeVersion) fail("no active version");

  if (s.version !== s.activeVersion) {
    fail(`version drift: ${s.version} != ${s.activeVersion}`);
  }

  if (s.status && s.status.includes("corrupt")) {
    fail("corrupt state detected");
  }

  console.log("[RELEASE GATE] OK");
  return true;
}

// בדיקת git clean
function gitCheck() {
  const out = execSync("git status --porcelain").toString().trim();
  if (out.length > 0) {
    fail("uncommitted changes exist");
  }
  console.log("[RELEASE GATE] git clean");
}

function run() {
  gitCheck();
  validate();
}

run();
