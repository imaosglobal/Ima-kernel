const fs = require("fs");
const path = require("path");

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

// מגדיר גרסה יציבה אחת בלבד כ- ACTIVE
function lockToStableVersion() {
  const state = load();

  const active = state.version || "unknown";

  state.activeVersion = active;
  state.safeVersion = state.safeVersion || active;

  state.policy = {
    singleSourceOfTruth: true,
    locked: true,
    rollbackAllowed: true
  };

  save(state);

  console.log("VERSION LOCKED:");
  console.log("ACTIVE =", state.activeVersion);
  console.log("SAFE   =", state.safeVersion);
}

// בדיקה שהמערכת תמיד עולה על ACTIVE
function validateRuntime() {
  const state = load();

  if (!state.activeVersion) {
    throw new Error("NO ACTIVE VERSION SET");
  }

  if (state.status === "corrupt") {
    console.log("ROLLBACK TO SAFE VERSION");
    state.version = state.safeVersion;
    state.status = "recovered";
    save(state);
  }

  return true;
}

module.exports = {
  lockToStableVersion,
  validateRuntime
};
