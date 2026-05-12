const fs = require("fs");
const crypto = require("crypto");

function hashFile(file) {
  const c = fs.readFileSync(file, "utf8");
  return crypto.createHash("sha256").update(c).digest("hex");
}

function loadState() {
  try {
    return JSON.parse(fs.readFileSync("./runtime/kernel_state.json","utf8"));
  } catch {
    return {};
  }
}

// השוואת מצב אמיתי (לא רק גרסה)
function diffCheck() {
  const files = [
    "./runtime/FS_CONTROLLER.js",
    "./runtime/VERSION_ENGINE.js",
    "./runtime/KERNEL_STATE.js"
  ];

  return files.map(f => ({
    file: f,
    hash: hashFile(f)
  }));
}

// החלטה מרכזית
function decide() {
  const state = loadState();
  const snapshot = diffCheck();

  const last = state.snapshot || [];

  const changed =
    JSON.stringify(snapshot) !== JSON.stringify(last);

  if (!changed) {
    return { action: "ignore", reason: "no real change" };
  }

  // רמת סיכון בסיסית
  const risky =
    snapshot.some(f => f.file.includes("ENTRYPOINT"));

  if (risky) {
    return { action: "hold", reason: "core file risk detected" };
  }

  return { action: "release", reason: "safe diff detected", snapshot };
}

module.exports = { decide, diffCheck };
