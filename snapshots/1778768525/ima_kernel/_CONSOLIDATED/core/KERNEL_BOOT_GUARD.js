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

// בודק אם תהליך רץ על גרסה מאושרת בלבד
function enforce() {
  const state = load();

  const active = state.activeVersion;
  const current = state.version;

  if (!active) {
    throw new Error("NO ACTIVE VERSION LOCKED");
  }

  // אם יש סטייה בגרסה → rollback ל-safe
  if (current !== active) {
    console.log("[BOOT GUARD] VERSION MISMATCH");
    console.log("ACTIVE:", active);
    console.log("CURRENT:", current);

    state.version = state.safeVersion || active;
    state.status = "rolled_back";

    save(state);

    console.log("[BOOT GUARD] rollback applied");
  } else {
    console.log("[BOOT GUARD] OK - version allowed:", active);
  }

  return true;
}

module.exports = { enforce };
