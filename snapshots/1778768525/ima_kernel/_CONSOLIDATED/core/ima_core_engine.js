const fs = require("fs");
const path = require("path");
const cp = require("child_process");
const crypto = require("crypto");

const ROOT = process.env.HOME + "/ima_kernel";
const LEGACY = ROOT + "/legacy";
const STATE = ROOT + "/core/state.json";

console.log("=== IMA CORE ENGINE BOOT ===");

// ============================
// SAFE EXEC
// ============================
function exec(cmd) {
  try {
    return cp.execSync(cmd, { encoding: "utf8", shell: true });
  } catch {
    return null;
  }
}

// ============================
// DIR SETUP (SINGLE TRUTH)
// ============================
function ensureDirs() {
  ["core", "runtime", "ui", "logs", "legacy", "sync"].forEach(d => {
    fs.mkdirSync(path.join(ROOT, d), { recursive: true });
  });
}

// ============================
// HASH (DEDUP ENGINE)
// ============================
function hash(content) {
  return crypto.createHash("sha256").update(content).digest("hex");
}

// ============================
// FULL SCAN
// ============================
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

// ============================
// AUTO CLASSIFY
// ============================
function classify(files) {
  const map = {};
  const duplicates = [];

  for (const f of files) {
    try {
      const data = fs.readFileSync(f);
      const h = hash(data);

      map[h] ||= [];
      map[h].push(f);
    } catch {}
  }

  for (const k in map) {
    if (map[k].length > 1) duplicates.push(map[k]);
  }

  return { map, duplicates };
}

// ============================
// AUTO MOVE NEW FILES INTO ROOT STRUCTURE
// ============================
function normalizeIntoRoot(files) {
  for (const f of files) {
    const rel = path.relative(ROOT, f);

    if (rel.startsWith("core") ||
        rel.startsWith("logs") ||
        rel.startsWith("runtime") ||
        rel.startsWith("ui") ||
        rel.startsWith("legacy")) continue;

    const target = path.join(LEGACY, rel.replace(/[\\/]/g, "__"));

    try {
      fs.renameSync(f, target);
    } catch {}
  }
}

// ============================
// BUILD SINGLE RUNTIME
// ============================
function buildRuntime() {
  const server = `
const express = require("express");
const app = express();
app.use(express.json());

let memory = [];

app.get("/health", (_, res) => {
  res.json({ ok: true, ts: Date.now() });
});

app.get("/memory", (_, res) => {
  res.json(memory);
});

app.post("/memory", (req, res) => {
  memory.push(req.body || {});
  res.json({ ok: true });
});

app.get("/", (_, res) => {
  res.send("IMA CORE ENGINE ACTIVE");
});

const PORT = 3000;
app.listen(PORT, () => console.log("IMA RUNNING", PORT));
`;

  fs.writeFileSync(ROOT + "/ima.js", server);
}

// ============================
// GIT SYNC
// ============================
function gitSync() {
  exec("git init");

  exec("git remote remove origin || true");
  exec("git remote add origin https://github.com/imaosglobal/Ima-kernel.git");

  exec("git add .");
  exec("git commit -m 'IMA CORE SYNC' || true");
}

// ============================
// NPM SYNC
// ============================
function npmSync() {
  const pkg = {
    name: "ima-kernel",
    version: "core-engine",
    main: "ima.js",
    scripts: {
      start: "node ima.js"
    },
    dependencies: {
      express: "latest"
    }
  };

  fs.writeFileSync(ROOT + "/package.json", JSON.stringify(pkg, null, 2));

  exec("npm install --silent");
}

// ============================
// DAEMON CONTROL
// ============================
function startDaemon() {
  exec("pkill -f ima.js || true");
  exec(`nohup node ${ROOT}/ima.js > ${ROOT}/logs/runtime.log 2>&1 &`);
}

// ============================
// STATE WRITE
// ============================
function writeState(meta) {
  fs.writeFileSync(STATE, JSON.stringify(meta, null, 2));
}

// ============================
// MAIN LOOP (SELF HEAL)
// ============================
function run() {
  ensureDirs();

  const files = scan(ROOT);
  const { duplicates } = classify(files);

  normalizeIntoRoot(files);

  buildRuntime();
  npmSync();
  gitSync();
  startDaemon();

  writeState({
    root: ROOT,
    files: files.length,
    duplicates: duplicates.length,
    ts: Date.now(),
    mode: "CORE_ENGINE_V1"
  });

  console.log("=== IMA CORE ENGINE READY ===");
  console.log({
    files: files.length,
    duplicates: duplicates.length
  });
}

// ============================
// BOOT
// ============================
run();

// ============================
// WATCHER (FUTURE SYNC)
// ============================
setInterval(run, 15000);
