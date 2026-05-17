#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA SINGLE CLEAN SYSTEM ==="

ROOT="$HOME/ima_kernel"

cd "$ROOT"

# -----------------------------------
# 1. HARD CLEAN
# -----------------------------------
echo "[1] stopping old processes"

pkill -9 -f node 2>/dev/null || true
pkill -9 -f watchdog 2>/dev/null || true
pkill -9 -f crond 2>/dev/null || true

sleep 2

# -----------------------------------
# 2. DISABLE OLD AUTO START
# -----------------------------------
echo "[2] disabling legacy boot"

mkdir -p "$HOME/.termux/boot_disabled"

mv "$HOME/.termux/boot/"* \
   "$HOME/.termux/boot_disabled/" \
   2>/dev/null || true

# -----------------------------------
# 3. CLEAN STRUCTURE
# -----------------------------------
echo "[3] preparing structure"

mkdir -p core
mkdir -p logs
mkdir -p runtime

# -----------------------------------
# 4. SINGLE SERVER
# -----------------------------------
echo "[4] creating runtime"

cat > "$ROOT/core/server.js" <<'EOJS'
const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();

const STATE = path.join(__dirname, "..", "runtime", "state.json");

function writeState() {
  fs.writeFileSync(
    STATE,
    JSON.stringify({
      status: "ONLINE",
      mode: "IMA_SINGLE_CLEAN",
      pid: process.pid,
      ts: Date.now()
    }, null, 2)
  );
}

app.get("/", (req, res) => {
  res.send("IMA SINGLE CLEAN ONLINE");
});

app.get("/health", (req, res) => {
  writeState();

  res.json({
    status: "ONLINE",
    mode: "IMA_SINGLE_CLEAN",
    pid: process.pid,
    ts: Date.now()
  });
});

const PORT = 7000;

app.listen(PORT, () => {
  writeState();
  console.log("[IMA] ONLINE :" + PORT);
});
EOJS

# -----------------------------------
# 5. SINGLE ENTRY
# -----------------------------------
echo "[5] creating entry"

cat > "$ROOT/ima.js" <<'EOJS'
require("./core/server");
EOJS

# -----------------------------------
# 6. PACKAGE.JSON
# -----------------------------------
echo "[6] package setup"

cat > "$ROOT/package.json" <<'EOJSON'
{
  "name": "ima-single-clean",
  "version": "1.0.0",
  "main": "ima.js",
  "type": "commonjs",
  "scripts": {
    "start": "node ima.js"
  },
  "dependencies": {
    "express": "^5.1.0"
  }
}
EOJSON

npm install --silent

# -----------------------------------
# 7. CLEAN START SCRIPT
# -----------------------------------
echo "[7] creating start.sh"

cat > "$ROOT/start.sh" <<'EOSH'
#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"

cd "$ROOT"

LOCK="$ROOT/runtime/kernel.lock"

if [ -f "$LOCK" ]; then
  PID=$(cat "$LOCK" 2>/dev/null || true)

  if ps -p "$PID" > /dev/null 2>&1; then
    echo "IMA ALREADY RUNNING"
    exit 0
  fi
fi

nohup node ima.js > logs/runtime.log 2>&1 &

PID=$!

echo "$PID" > "$LOCK"

sleep 2

curl -s http://127.0.0.1:7000/health || echo "BOOT FAILED"
EOSH

chmod +x "$ROOT/start.sh"

# -----------------------------------
# 8. GIT CLEAN SNAPSHOT
# -----------------------------------
echo "[8] git snapshot"

if [ ! -d "$ROOT/.git" ]; then
  git init
fi

git add -A

git commit -m "IMA SINGLE CLEAN $(date +%s)" || true

git tag -f SINGLE_CLEAN_SYSTEM

# -----------------------------------
# 9. START SYSTEM
# -----------------------------------
echo "[9] starting runtime"

bash "$ROOT/start.sh"

# -----------------------------------
# 10. VERIFY
# -----------------------------------
echo ""
echo "=== VERIFY ==="

echo ""
echo "[HEALTH]"
curl -s http://127.0.0.1:7000/health

echo ""
echo ""

echo "[PROCESS]"
ps aux | grep "node ima.js" | grep -v grep || true

echo ""
echo ""

echo "[LOCK]"
cat "$ROOT/runtime/kernel.lock"

echo ""
echo ""

echo "[GIT]"
git log --oneline -1

echo ""
echo "=== IMA SINGLE CLEAN READY ==="

