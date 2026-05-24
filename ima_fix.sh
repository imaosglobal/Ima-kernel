#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_kernel || exit 1

echo "[IMA FIX] starting system repair..."

# 1. יצירת תיקיות חסרות
mkdir -p kernel/cloud
mkdir -p kernel/vibe
mkdir -p kernel/plugins
mkdir -p logs

# 2. תיקון brain fallback אם חסר
if [ ! -f kernel/brain/brain_engine.js ]; then
cat > kernel/brain/brain_engine.js <<'JS'
module.exports = {}
console.log("[BRAIN] fallback loaded")
JS
fi

# 3. תיקון cloud bridge
if [ ! -f kernel/cloud/cloud_bridge.js ]; then
cat > kernel/cloud/cloud_bridge.js <<'JS'
const https = require("https")

function sendToCloud(prompt){
  return Promise.resolve("[cloud disabled - stub]")
}

module.exports = { sendToCloud }
JS
fi

# 4. תיקון vibe gateway
if [ ! -f kernel/vibe/termux_gateway.js ]; then
cat > kernel/vibe/termux_gateway.js <<'JS'
function handle(input){
  console.log("[VIBE]", input)
  return { type:"ok" }
}

module.exports = { handle }
JS
fi

# 5. מניעת קריסת ima.js
touch ima.js

if ! grep -q "termux_gateway" ima.js; then
echo 'require("./kernel/vibe/termux_gateway")' >> ima.js
fi

# 6. kill + restart נקי
pkill -f node

sleep 1

nohup node ~/ima_kernel/ima.js > logs/runtime.log 2>&1 &

echo "[IMA FIX] system restarted safely"
