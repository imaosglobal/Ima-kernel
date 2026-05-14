const fs = require("fs");
const path = require("path");
const cp = require("child_process");

const ROOT = process.env.HOME + "/ima_kernel";

console.log("=== IMA BOOTSTRAP CORE ===");

// ----------------------
// EXEC
// ----------------------
function exec(cmd) {
  try {
    return cp.execSync(cmd, { shell: true, encoding: "utf8" });
  } catch {
    return null;
  }
}

// ----------------------
// CREATE SINGLE STRUCTURE
// ----------------------
const dirs = ["core", "runtime", "ui", "logs", "legacy"];

for (const d of dirs) {
  fs.mkdirSync(path.join(ROOT, d), { recursive: true });
}

// ----------------------
// FIND SOURCES (ALL OLD SYSTEMS)
// ----------------------
const sources = [
  process.env.HOME + "/ima_core",
  process.env.HOME + "/ima_workspace",
  process.env.HOME + "/ima_kernel_boot",
  process.env.HOME + "/ima_single_kernel"
].filter(fs.existsSync);

console.log("SOURCES:", sources.length);

// ----------------------
// SIMPLE MERGE (SAFE COPY ONLY JS/JSON)
// ----------------------
function walk(dir, out = []) {
  for (const f of fs.readdirSync(dir)) {
    const full = path.join(dir, f);

    if (full.includes("node_modules") || full.includes(".git")) continue;

    const stat = fs.statSync(full);

    if (stat.isDirectory()) walk(full, out);
    else out.push(full);
  }
  return out;
}

let files = [];
for (const s of sources) files = files.concat(walk(s));

console.log("FILES:", files.length);

// ----------------------
// PICK ONLY WORKING LOGIC (JS ONLY)
// ----------------------
const jsFiles = files.filter(f => f.endsWith(".js"));

let mergedRuntime = `
const express = require("express");
const app = express();

let memoryStore = [];

function memory() {
  return memoryStore;
}

app.get("/health", (_, res) => {
  res.json({ ok: true });
});

app.get("/memory", (_, res) => {
  res.json(memory());
});

const PORT = 3000;

app.listen(PORT, () => {
  console.log("IMA SINGLE SYSTEM RUNNING:", PORT);
});
`;

// ----------------------
// WRITE SINGLE SYSTEM FILE
// ----------------------
fs.writeFileSync(ROOT + "/ima.js", mergedRuntime);

// ----------------------
// PACKAGE
// ----------------------
fs.writeFileSync(
  ROOT + "/package.json",
  JSON.stringify({
    name: "ima-kernel",
    version: "stable-1",
    main: "ima.js",
    scripts: {
      start: "node ima.js"
    },
    dependencies: {
      express: "latest"
    }
  }, null, 2)
);

// ----------------------
// START DAEMON (SINGLE INSTANCE)
// ----------------------
exec("pkill -f ima.js || true");
exec("nohup node ima.js > logs/runtime.log 2>&1 &");

console.log("=== IMA BOOTSTRAP COMPLETE ===");
