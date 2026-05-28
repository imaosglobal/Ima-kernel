#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$HOME/ima_kernel"
TARGET="$ROOT/ima_orchestrator.js"

mkdir -p "$ROOT"
mkdir -p "$ROOT/memory"
mkdir -p "$ROOT/logs"
mkdir -p "$ROOT/backups"
mkdir -p "$ROOT/patches"

pkg install -y zip >/dev/null 2>&1 || true

if [ -f "$TARGET" ]; then
  echo "[UPDATE] existing orchestrator found"
  cp "$TARGET" "$ROOT/backups/ima_orchestrator_$(date +%s).js.bak"
else
  echo "[CREATE] new orchestrator"
fi

cat > "$TARGET" <<'NODE'
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const ROOT = "/data/data/com.termux/files/home/ima_kernel";

function walk(dir, arr = []) {
  let files = [];

  try {
    files = fs.readdirSync(dir);
  } catch (e) {
    return arr;
  }

  for (const file of files) {

    const full = path.join(dir, file);

    try {

      const stat = fs.statSync(full);

      if (stat.isDirectory()) {

        if (
          file === "node_modules" ||
          file === ".git" ||
          file === "_graveyard"
        ) continue;

        walk(full, arr);

      } else {

        arr.push(full);

      }

    } catch (e) {}
  }

  return arr;
}

function safeRead(file) {

  try {

    if (fs.statSync(file).size > 100000) {
      return "[FILE TOO LARGE]";
    }

    return fs.readFileSync(file, "utf8");

  } catch (e) {

    return "[BINARY OR UNREADABLE]";
  }
}

function scanProject() {

  console.log("\\n[SCAN] scanning project...\\n");

  const files = walk(ROOT);

  const result = [];

  for (const file of files) {

    const ext = path.extname(file);

    if (
      [
        ".js",
        ".json",
        ".md",
        ".txt",
        ".yml",
        ".yaml",
        ".ts"
      ].includes(ext)
    ) {

      result.push({
        path: file,
        content: safeRead(file)
      });

    }
  }

  return result;
}

function detectProblems(files) {

  const problems = [];

  for (const f of files) {

    const c = f.content;

    if (typeof c !== "string") continue;

    if (
      c.includes("TODO") ||
      c.includes("FIXME")
    ) {

      problems.push({
        file: f.path,
        issue: "TODO/FIXME FOUND"
      });
    }

    if (
      c.includes("<<<<<<<") ||
      c.includes("=======")
    ) {

      problems.push({
        file: f.path,
        issue: "MERGE CONFLICT"
      });
    }
  }

  return problems;
}

function createBrainFile(files) {

  const summary = files
    .map(f => f.path)
    .join("\\n");

  fs.writeFileSync(
    `${ROOT}/memory/project_map.md`,
    summary
  );

  console.log("\\n[BRAIN MAP CREATED]");
}

function backupProject() {

  const stamp = Date.now();

  const zipPath =
    `${ROOT}/backups/ima_backup_${stamp}.zip`;

  console.log("\\n[BACKUP]\\n");

  try {

    execSync(
      `cd ${ROOT} && zip -r ${zipPath} . -x "*node_modules*"`,
      { stdio: "inherit" }
    );

  } catch (e) {}

  console.log("\\n[SAVED]", zipPath);
}

function validateNode() {

  console.log("\\n[NODE CHECK]\\n");

  try {

    execSync("node -v", {
      stdio: "inherit"
    });

  } catch (e) {

    console.log("NODE NOT INSTALLED");
  }
}

function validateNpm() {

  console.log("\\n[NPM CHECK]\\n");

  try {

    execSync("npm -v", {
      stdio: "inherit"
    });

  } catch (e) {

    console.log("NPM NOT INSTALLED");
  }
}

function tryStartServer() {

  console.log("\\n[SERVER TEST]\\n");

  const candidates = [
    "server.js",
    "index.js",
    "main.js"
  ];

  for (const c of candidates) {

    const full = path.join(ROOT, c);

    if (fs.existsSync(full)) {

      console.log("[FOUND]", full);

      try {

        execSync(
          `timeout 10 node ${full}`,
          { stdio: "inherit" }
        );

      } catch (e) {}

      return;
    }
  }

  console.log("NO ENTRY FILE FOUND");
}

function createUnifiedLauncher() {

  const launcher = `#!/data/data/com.termux/files/usr/bin/bash
cd ~/ima_kernel
node ima_orchestrator.js
`;

  fs.writeFileSync(
    `${ROOT}/boot.sh`,
    launcher
  );

  try {

    execSync(
      `chmod +x ${ROOT}/boot.sh`
    );

  } catch (e) {}

  console.log("\\n[BOOT SCRIPT READY]");
}

async function run() {

  console.log("\\n========================");
  console.log("IMA ORCHESTRATOR");
  console.log("========================\\n");

  validateNode();
  validateNpm();

  const files = scanProject();

  console.log("\\nFILES:", files.length);

  const problems = detectProblems(files);

  console.log("\\nPROBLEMS:", problems.length);

  for (const p of problems) {

    console.log(
      "-",
      p.issue,
      "=>",
      p.file
    );
  }

  createBrainFile(files);
  backupProject();
  tryStartServer();
  createUnifiedLauncher();

  console.log("\\n[DONE]\\n");
}

run();
NODE

chmod +x "$TARGET"

cat > "$ROOT/run.sh" <<'RUN'
#!/data/data/com.termux/files/usr/bin/bash
cd ~/ima_kernel
node ima_orchestrator.js
RUN

chmod +x "$ROOT/run.sh"

cd "$ROOT"
node ima_orchestrator.js

