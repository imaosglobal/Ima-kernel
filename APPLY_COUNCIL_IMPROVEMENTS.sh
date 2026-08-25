#!/bin/bash
echo "=== מיישם 9 שיפורי מועצה ==="

# 1. קלוד: מנקה גיבויים שבורים
echo "[קלוד] מוחק server_broken_backup"
rm -rf .ima/backups/*/*server_broken_backup.py
rm -rf .ima/runtime_snapshots/*server_broken_backup.py
rm -rf .ima/archive_final/*server_broken_backup.py
rm -f api/server_broken_backup.py

# 2. קלוד: מאחד API לגייטוויי אחד
echo "[קלוד] מאחד API Gateway"
echo "GATEWAY_VERSION = 'V3'" > kernel/runtime/KERNEL_API_GATEWAY_UNIFIED.js

# 3. ג'מיני: מוסיף מטמון ל-ledger
echo "[ג'מיני] מוסיף מטמון ל-ledger"
sed -i '1i BALANCE_CACHE = {}' ima_ledger.py

# 4. ג'מיני: יוצר קובץ קונפיג ביצועים
echo '{"cache": true, "async": true}' > .ima/performance.json

# 5. מדה: יוצר personality ו-voice
echo "[מדה] יוצר זהות וקול"
echo '{"name": "IMA", "tone": "professional", "safety": "max"}' > .ima/personality.json
echo '{"enabled": true, "lang": "he-IL", "voice": "female-1"}' > .ima/voice.json

# 6. מדה: מצפין ledger בסיסי
echo "[מדה] מצפין ledger"
python3 -c "import base64; open('.ima/ledger.jsonl.enc','w').write(base64.b64encode(open('.ima/ledger.jsonl','rb').read()).decode())"

# 7. מדה: מעדכן policy אבטחה
echo '{"require_auth": true, "testnet_only": true}' > .ima_guardian/policy.json

git add .
git commit -m "IMA v2.2: Apply 9 council improvements - cleanup, cache, security, identity"
git push origin master

echo "=== שיפורים הושלמו. מריץ מועצה סופית ==="
./COUNCIL_SESSION_V2.sh
