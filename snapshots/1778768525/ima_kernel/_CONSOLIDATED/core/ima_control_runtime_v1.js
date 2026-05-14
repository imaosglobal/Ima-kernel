const fs = require("fs");
const cp = require("child_process");
const path = require("path");
const crypto = require("crypto");

const ROOT = process.env.HOME + "/ima_workspace";
const STATE = path.join(ROOT, "core/control_state.json");
const LOCK = path.join(ROOT, "core/workspace.lock.json");

console.log("\n==============================");
console.log("IMA CONTROL RUNTIME v1");
console.log("==============================\n");

// ===============================
// EXEC
// ===============================
function exec(cmd) {
  try {
    return cp.execSync(cmd, {
      cwd: ROOT,
      shell: true,
      encoding: "utf8"
    }).toString().trim();
  } catch {
    return null;
  }
}

// ===============================
// SAFE FS
// ===============================
function safeWrite(file, data) {
  const full = path.join(ROOT, file);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, data);
}

// ===============================
// LOCK WORKSPACE (soft enforcement)
// ===============================
const lock = {
  root: ROOT,
  mode: "IMA_CONTROL_RUNTIME_V1",
  timestamp: Date.now()
};

safeWrite("core/workspace.lock.json", JSON.stringify(lock, null, 2));

// ===============================
// SCAN SYSTEM
// ===============================
function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;

  for (const f of fs.readdirSync(dir)) {
    const full = path.join(dir, f);
    const rel = path.relative(ROOT, full);

    if (rel.includes("node_modules") || rel.includes(".git")) continue;

    let st;
    try { st = fs.statSync(full); } catch { continue; }

    if (st.isDirectory()) walk(full, out);
    else out.push(rel);
  }

  return out;
}

const files = walk(ROOT);
console.log("FILES:", files.length);

// ===============================
// HASH DUPLICATES
// ===============================
const map = {};
const duplicates = [];

for (const f of files) {
  try {
    const buf = fs.readFileSync(path.join(ROOT, f));
    const h = crypto.createHash("sha256").update(buf).digest("hex");

    map[h] ||= [];
    map[h].push(f);
  } catch {}
}

for (const k in map) {
  if (map[k].length > 1) duplicates.push(map[k]);
}

console.log("DUPLICATE GROUPS:", duplicates.length);

// ===============================
// CANONICAL SELECTION (REAL PRIORITY)
// ===============================
function score(f) {
  let s = 0;
  if (f.includes("runtime")) s += 6;
  if (f.includes("engine")) s += 5;
  if (f.includes("server")) s += 5;
  if (f.includes("daemon")) s += 4;
  if (f.endsWith(".js")) s += 2;
  return s;
}

const runtimeCandidates = files
  .filter(f => f.endsWith(".js"))
  .sort((a, b) => score(b) - score(a));

const canonical = runtimeCandidates[0] || "server.js";

console.log("CANONICAL:", canonical);

// ===============================
// DAEMON CONTROL (SINGLE INSTANCE)
// ===============================
const daemon = canonical;

console.log("DAEMON TARGET:", daemon);

// kill old instances (best effort)
exec(`pkill -f "${daemon}" || true`);

// start fresh daemon
exec(`nohup node "${daemon}" > logs/runtime.log 2>&1 &`);

// ===============================
// WRITE SYSTEM STATE
// ===============================
const state = {
  files: files.length,
  duplicates: duplicates.length,
  canonical,
  daemon,
  timestamp: Date.now()
};

safeWrite("core/control_state.json", JSON.stringify(state, null, 2));
safeWrite("logs/duplicates.json", JSON.stringify(duplicates, null, 2));

// ===============================
// HEALTH CHECK
// ===============================
let health = false;
const test = exec("node --check server.js");
health = test !== null;

state.health = health;

// update final state
safeWrite("core/control_state.json", JSON.stringify(state, null, 2));

// ===============================
// OUTPUT
// ===============================
console.log("\n==============================");
console.log("IMA CONTROL RUNTIME READY");
console.log("==============================");
console.log(state);
