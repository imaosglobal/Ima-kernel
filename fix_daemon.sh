#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA DAEMON FIX ==="

cd ~/ima_kernel

echo "[1] Patching ima_daemon.py"

python3 - <<'PY'
from pathlib import Path

p = Path("ima_daemon.py")
s = p.read_text()

# remove broken escaped newlines
s = s.replace("\\n", "\n")

# normalize duplicate processing print
s = s.replace(
'''print("PROCESSING:", qid, question)
                print("PROCESSING:", qid, question)
                ask(question, qid=qid)''',
'''print("PROCESSING:", qid, question)
                ask(question, qid=qid)'''
)

# add duplicate ANSWER protection if missing
if 'x.get("type") == "ANSWER"' not in s:
    marker = '''                qid = data.get("id", e.get("ts"))
'''
    insert = '''                qid = data.get("id", e.get("ts"))

                if any(
                    x.get("type") == "ANSWER"
                    and x.get("data", {}).get("id") == qid
                    for x in events
                ):
                    continue
'''
    s = s.replace(marker, insert)

p.write_text(s)
PY

echo "[2] Compile check"

python3 -m py_compile ima_daemon.py ima_system.py

echo "[3] Stop old daemon"

pkill -f ima_daemon.py || true

sleep 1

echo "[4] Start daemon"

nohup python3 ima_daemon.py > .ima/daemon.log 2>&1 &

sleep 2

echo "[5] Test"

echo '{"ts":"test_fix","type":"QUESTION","data":{"id":"fix001","text":"בדיקת תיקון"}}' >> .ima/ledger.jsonl

sleep 2

echo "=== RESULT ==="
grep fix001 .ima/ledger.jsonl || true

echo "=== DAEMON LOG ==="
tail -20 .ima/daemon.log || true

echo "=== DONE ==="
