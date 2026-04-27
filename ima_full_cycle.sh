#!/data/data/com.termux/files/usr/bin/bash

echo "🧠 IMA FULL CYCLE START"

# ---------------- STEP 1: SYSTEM CHECK ----------------
echo "🔍 Checking files..."
[ -f ima_stable_brain.js ] || echo "⚠ missing ima_stable_brain.js"
[ -f memory.json ] || echo '{"memory":[]}' > memory.json

# ---------------- STEP 2: RUN IMA ----------------
echo "🚀 Running IMA..."
node ima_stable_brain.js "daily evolution"

# ---------------- STEP 3: UPDATE STATE ----------------
echo "🔄 Updating config..."
cat > ima_config.json <<CFG
{
  "last_run": "$(date +%s)",
  "status": "active",
  "mode": "local"
}
CFG

# ---------------- STEP 4: GIT SYNC ----------------
echo "📦 Syncing with Git..."

git add .

git commit -m "IMA auto cycle $(date +%s)" 2>/dev/null

git push origin main 2>/dev/null

# ---------------- STEP 5: REPORT ----------------
echo "📊 STATUS:"
git status -s

echo "🧠 IMA FULL CYCLE DONE"
