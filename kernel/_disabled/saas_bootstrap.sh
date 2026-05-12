#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== SAAS BOOTSTRAP START ==="

cd ~/ima_core/kernel

# 1. stop server
pkill -f node || true

# 2. create db (simple + stable fallback)
cat > db_memory.js << 'JS'
const fs = require("fs");
const FILE = "./users.json";

function load() {
  if (!fs.existsSync(FILE)) fs.writeFileSync(FILE, "{}");
  return JSON.parse(fs.readFileSync(FILE));
}

function save(data) {
  fs.writeFileSync(FILE, JSON.stringify(data, null, 2));
}

module.exports = {
  getUser: (key, cb) => {
    const db = load();
    cb(null, db[key]);
  },

  createUser: (key, cb) => {
    const db = load();
    db[key] = { usage: 0, plan: "free", createdAt: Date.now() };
    save(db);
    cb(null, db[key]);
  },

  updateUser: (key, data, cb) => {
    const db = load();
    db[key] = data;
    save(db);
    cb(null, data);
  }
};
JS

# 3. create server (clean safe version)
cat > server.js << 'JS'
const express = require("express");
const app = express();
const db = require("./db_memory");

app.use(express.json());

app.post("/signup", (req, res) => {
  const key = Math.random().toString(36).substring(2);

  db.createUser(key, () => {
    res.json({ apiKey: key });
  });
});

app.post("/run", (req, res) => {
  const key = req.headers["x-api-key"];
  const task = req.body?.task;

  if (!key) return res.json({ error: "Missing API key" });
  if (!task) return res.json({ error: "Missing task" });

  db.getUser(key, (err, user) => {
    if (!user) return res.json({ error: "Invalid API key" });

    if (user.plan !== "paid" && user.usage >= 100) {
      return res.json({ error: "Limit reached (upgrade required)" });
    }

    user.usage++;

    db.updateUser(key, user, () => {
      res.json({
        ok: true,
        result: "Processed: " + task,
        usage: user.usage,
        plan: user.plan
      });
    });
  });
});

app.listen(4000, () => {
  console.log("SAAS RUNNING ON 4000");
});
JS

# 4. start server
node server.js &

sleep 2

# 5. test signup
echo "[TEST] signup"
RESP=$(curl -s -X POST http://localhost:4000/signup)
echo $RESP

KEY=$(echo $RESP | grep -o '"apiKey":"[^"]*' | cut -d'"' -f4)

echo "[TEST] run"
curl -s -X POST http://localhost:4000/run \
  -H "x-api-key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"task":"hello system"}'

echo
echo "=== SAAS READY ==="
