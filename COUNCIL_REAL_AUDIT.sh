#!/bin/bash
echo "========================================"
echo "IMA COUNCIL REAL AUDIT - $(date)"
echo "========================================"

echo ""
echo "[1. ספירת קבצים]"
find . -type f | wc -l

echo ""
echo "[2. בדיקת CANONICAL - האם כל 19 קבצים קיימים]"
REGISTRY=".ima/CANONICAL_AUTHORITY/governance/CANONICAL_REGISTRY.json"
if [ -f "$REGISTRY" ]; then
  python3 -c "import json; r=json.load(open('$REGISTRY')); print('Components in registry:', len(r.get('allowed_components',[])))"
else
  echo "REGISTRY NOT FOUND"
fi

echo ""
echo "[3. בדיקת HASH - מריץ את האורכסטרטור האמיתי]"
python3 .ima/CANONICAL_AUTHORITY/evolution/SELF_EVOLUTION/REPAIR_ENGINE/IMA_CANONICAL_CHAIN_ORCHESTRATOR.py

echo ""
echo "[4. בדיקת CHILD SAFETY - ספירה]"
find . -name "*child*" -type f | wc -l
find . -name "*child*" -type f

echo ""
echo "[5. בדיקת סודות קשיחים]"
grep -ri "password\|secret\|private_key" . --include="*.py" --include="*.json" | grep -v ".git" | wc -l

echo ""
echo "[6. בדיקת UI חי]"
curl -s http://localhost:8080 | grep "IMA Bank" || echo "UI NOT RUNNING"

echo ""
echo "[7. בדיקת GIT]"
git log -1 --oneline

echo ""
echo "=== END AUDIT ==="
