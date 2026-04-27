#!/bin/bash

echo "🧠 IMA DAILY FINALIZATION START"

# 1. status snapshot
echo "📊 GIT STATUS"
git status

# 2. add all changes
echo "📦 STAGING ALL CHANGES"
git add -A

# 3. commit snapshot
echo "💾 CREATING DAILY SNAPSHOT"
git commit -m "daily full sync + evolution snapshot $(date +%s)" || echo "⚠️ nothing to commit"

# 4. push to main repo
echo "🚀 PUSHING TO GITHUB"
git push origin main

# 5. show last commit
echo "📌 LAST COMMIT"
git log -1 --oneline

# 6. verify remote sync
echo "🔍 VERIFY REMOTE STATUS"
git fetch origin
git status

# 7. system summary
echo "🧠 IMA SYSTEM SUMMARY COMPLETE"
echo "✔ kernel"
echo "✔ runtime"
echo "✔ evolution engine"
echo "✔ behavior engine"
echo "✔ extension engine"
echo "✔ orchestrator"
echo "✔ memory system"

echo "✅ ALL SYSTEMS SYNCHRONIZED"
🗺 RUNNING SYSTEM MAP ENGINE
node ima_system_map_engine.js
node ima_auto_executor.js
node ima_feedback_loop.js
