#!/bin/bash

echo "🧠 IMA DAILY FINALIZER START"

# 1. בדיקת שרת
echo "🔍 checking server..."
if ! curl -s http://localhost:4000/ima/run -X POST \
  -H "Content-Type: application/json" \
  -d '{"message":"health"}' > /dev/null; then
  echo "❌ server not responding"
  exit 1
fi

echo "✅ server OK"

# 2. בדיקת brain endpoint
echo "🧠 checking brain endpoint..."
BRAIN=$(curl -s http://localhost:4000/ima/brain)

if [[ $BRAIN == *"Cannot GET"* ]]; then
  echo "⚠️ brain missing, injecting..."

  printf '\nconst knowledge = require("./kernel/knowledge");\napp.get("/ima/brain", (req,res)=>{\n  try {\n    res.json(knowledge.summarize());\n  } catch(e) {\n    res.json({ error: e.message });\n  }\n});\n' >> world_api.js

  echo "🔧 injected brain endpoint"
fi

# 3. Git sync
echo "📦 syncing to git..."
git add .
git commit -m "IMA daily sync $(date +%s)" || echo "no changes"
git push

# 4. learning log update
echo "📚 ensuring learning exists..."
if [ ! -f learning_log.json ]; then
  echo "[]" > learning_log.json
fi

# 5. final test
echo "🧪 final API test..."
curl -s http://localhost:4000/ima/run -X POST \
-H "Content-Type: application/json" \
-d '{"message":"final test"}'

echo ""
echo "🏁 IMA DAILY FINISH COMPLETE"
