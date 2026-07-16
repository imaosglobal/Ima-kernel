#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA CONVERSATION CORE REPAIR ==="

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "[1] Backup current files"

mkdir -p .ima/repair_backup

cp -f ima_master_runtime.py .ima/repair_backup/ 2>/dev/null || true
cp -f ima_mom.py .ima/repair_backup/ 2>/dev/null || true
cp -f api/server.py .ima/repair_backup/ 2>/dev/null || true


echo "[2] Create clean conversation router"

mkdir -p core

cat > core/conversation_router.py <<'PY'
def route(message):

    q = (message or "").strip()

    if q in ["היי","שלום","הי","בוקר טוב","ערב טוב"]:
        return "שלום אורי. אני כאן. מה ניצור או נחקור היום?"

    if "חלל" in q:
        return "החלל הוא מרחב של חומר, זמן ואפשרויות. אנחנו חוקרים אותו דרך פיזיקה, דמיון ושאלות על המקום שלנו ביקום."

    if "מה נשמע" in q:
        return "אני מחוברת. הליבה פעילה והשיחה עובדת."

    if "מי את" in q or "מה זה IMA" in q:
        return "אני IMA. מערכת שנבנית סביב שיחה, למידה, יצירה וחיבור בין תחומים."

    return None
PY


echo "[3] Patch server brain"

python3 <<'PY'
from pathlib import Path

p=Path("api/server.py")

s=p.read_text(encoding="utf-8")

if "from core.conversation_router import route" not in s:
    s=s.replace(
        "import json,time",
        "import json,time\nfrom core.conversation_router import route"
    )

old='answer = product_gateway.ask(question)'

new='''answer = product_gateway.ask(question)

try:
    clean = route(question)
    if clean:
        answer = {
            "response": clean,
            "status": "OK"
        }
except Exception:
    pass'''

s=s.replace(old,new)

p.write_text(s,encoding="utf-8")

PY


echo "[4] Remove memory echo display"

python3 <<'PY'
from pathlib import Path

for f in [
"ima_master_runtime.py",
"archive/ima_master_runtime_before_learning_router.py"
]:
    p=Path(f)
    if p.exists():
        s=p.read_text(encoding="utf-8")
        s=s.replace('"הקשר מזיכרון:\\n" +','"" +')
        p.write_text(s,encoding="utf-8")
PY


echo "[5] Restart API"

pkill -f "api/server.py" || true

sleep 2

nohup python3 api/server.py > ima_api.log 2>&1 &

sleep 3


echo "[6] Test core"

curl -s http://127.0.0.1:8080/health

echo
echo "=== TEST CHAT ==="

curl -s -X POST http://127.0.0.1:8080/ask \
-H "Content-Type: application/json" \
-d '{"message":"שלום אמא"}'

echo
echo
echo "=== DONE ==="
echo "Run UI:"
echo "cd ~/ima_kernel/ima-ui && npm run dev"
