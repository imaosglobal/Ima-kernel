const fs = require("fs");
const path = require("path");

const ROOT = process.env.HOME + "/ima_kernel";
const STATE = ROOT + "/core/stable_state.json";

let LOCK = false;

// --------------------
// FREEZE SYSTEM
// --------------------
function freeze() {
  LOCK = true;
}

function unfreeze() {
  LOCK = false;
}

// --------------------
// SAFE SCAN (READ ONLY)
// --------------------
function scan(dir, out = []) {
  if (!fs.existsSync(dir)) return out;

  for (const f of fs.readdirSync(dir)) {
    const full = path.join(dir, f);

    if (full.includes("node_modules") || full.includes(".git")) continue;

    try {
      const st = fs.statSync(full);

      if (st.isDirectory()) scan(full, out);
      else out.push(full);

    } catch {}
  }

  return out;
}

// --------------------
// SNAPSHOT ENGINE
// --------------------
function snapshot(files) {
  return {
    ts: Date.now(),
    count: files.length,
    files: files.slice(0, 50) // לא להציף
  };
}

// --------------------
// PLAN (NOT EXECUTE)
// --------------------
function plan(files) {
  const duplicates = {};

  for (const f of files) {
    const name = path.basename(f);

    duplicates[name] ||= 0;
    duplicates[name]++;
  }

  const dupList = Object.entries(duplicates)
    .filter(([_, c]) => c > 1)
    .map(([k, v]) => ({ file: k, count: v }));

  return {
    duplicates: dupList.length
  };
}

// --------------------
// SAFE RUN CYCLE
// --------------------
function cycle() {
  if (LOCK) return;

  freeze();

  const files = scan(ROOT);
  const snap = snapshot(files);
  const analysis = plan(files);

  fs.writeFileSync(STATE, JSON.stringify({
    snapshot: snap,
    analysis,
    mode: "STABLE_V2"
  }, null, 2));

  console.log("STABLE CYCLE:", snap.count, "files");

  unfreeze();
}

// --------------------
// BOOT
// --------------------
console.log("=== IMA STABLE CORE V2 START ===");

cycle();

setInterval(cycle, 10000);
