#!/data/data/com.termux/files/usr/bin/bash

set -e

BASE=~/ima_kernel
SERVER="$BASE/server.js"
ENGINE="$BASE/kernel/knowledge_engine.js"
MEM="$BASE/kernel/core/memory.js"

echo "[1/5] checking existing knowledge_engine..."

if [ ! -f "$ENGINE" ]; then
cat > "$ENGINE" << 'EOF2'
const memory = require("./core/memory");

function handle(input) {
  const mem = memory.load();

  if (!mem.history) mem.history = [];

  const match = mem.history.find(m =>
    JSON.stringify(m).includes(input)
  );

  if (match) {
    return {
      status: "FOUND",
      answer: match
    };
  }

  memory.add({
    query: input,
    result: "stored new knowledge",
    type: "auto"
  });

  return {
    status: "NEW",
    answer: "נוסף לזיכרון"
  };
}

module.exports = { handle };
EOF2
echo "[OK] knowledge_engine created"
else
echo "[OK] knowledge_engine already exists"
fi

echo "[2/5] patching server.js safely..."

grep -q "knowledge_engine" "$SERVER" || cat >> "$SERVER" << 'EOF3'

const knowledge = require("./kernel/knowledge_engine");

app.post("/ask", (req, res) => {
  try {
    const input = req.body.input || "";
    const result = knowledge.handle(input);
    res.json(result);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});
EOF3

echo "[3/5] ensuring memory compatibility..."

sed -i 's/memory\.memory/memory.history/g' "$SERVER" || true

echo "[4/5] restarting kernel..."

pkill -f server.js || true
sleep 1
nohup node "$SERVER" > "$BASE/runtime/logs/server.log" 2>&1 &

sleep 2

echo "[5/5] health check..."
curl -s http://127.0.0.1:3000/health || echo "server not responding"

echo ""
echo "[DONE] encyclopedia layer active"
