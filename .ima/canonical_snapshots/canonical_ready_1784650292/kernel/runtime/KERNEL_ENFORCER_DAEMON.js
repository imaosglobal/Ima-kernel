const fs = require("fs");

const STATE_FILE = "./runtime/kernel_state.json";

function load() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, "utf8"));
  } catch {
    return {};
  }
}

function save(s) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(s, null, 2));
}

function checkAndEnforce() {
  const state = load();

  if (!state.activeVersion) return;

  const active = state.activeVersion;
  const current = state.version;

  if (current !== active) {
    console.log("[ENFORCER] drift detected");

    state.version = state.safeVersion || active;
    state.status = "auto_rollback";

    save(state);

    console.log("[ENFORCER] rollback applied to:", state.version);
  }
}

function start() {
  console.log("=== KERNEL ENFORCER DAEMON STARTED ===");

  setInterval(checkAndEnforce, 2000);
}

start();
