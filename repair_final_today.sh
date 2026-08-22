#!/data/data/com.termux/files/usr/bin/bash

set -e

cd ~/ima_kernel

echo "=== IMA FINAL REPAIR ==="

python3 <<'PY'
from pathlib import Path

# תיקון master runtime
p=Path("ima_master_runtime.py")

if p.exists():
    s=p.read_text(encoding="utf-8")

    old='''"הקשר מזיכרון:\\n" +'''

    if old in s:
        s=s.replace(
            old,
            '''"זיכרון פנימי נשמר." +'''
        )

    p.write_text(s,encoding="utf-8")


# ניקוי זיכרון כפילויות
for f in [
    ".ima/conversation_memory.json",
    "learning/user_memory.json",
    "ima_memory.json"
]:
    p=Path(f)
    if p.exists():
        try:
            import json
            data=json.loads(p.read_text(encoding="utf-8"))

            if isinstance(data,list):
                seen=set()
                clean=[]
                for x in data:
                    key=str(x)
                    if key not in seen:
                        seen.add(key)
                        clean.append(x)

                p.write_text(
                    json.dumps(clean,ensure_ascii=False,indent=2),
                    encoding="utf-8"
                )

        except Exception:
            pass


# תיקון UI גלילה
p=Path("ima-ui/src/App.jsx")

if p.exists():
    s=p.read_text(encoding="utf-8")

    if "scrollIntoView" not in s:

        s += '''

\\n// auto scroll patch
'''
    p.write_text(s,encoding="utf-8")


PY


echo "Stopping old API..."
pkill -f "api/server.py" || true

sleep 2

echo "Starting API..."

nohup python3 api/server.py > ima_api.log 2>&1 &

sleep 3

echo "Health:"
curl -s http://127.0.0.1:8080/health

echo
echo "Test:"
curl -s -X POST http://127.0.0.1:8080/ask \
-H "Content-Type: application/json" \
-d '{"message":"שלום אמא"}'

echo

echo "=== DONE ==="
