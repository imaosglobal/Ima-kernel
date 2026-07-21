#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== IMA RELEASE REPAIR START ==="

ROOT=$(pwd)
DATE=$(date +%Y%m%d_%H%M%S)

echo "[1/10] Backup"
mkdir -p .ima/backups/$DATE
cp api/server.py .ima/backups/$DATE/ 2>/dev/null || true
cp ima_master_runtime.py identity_context.py conversation_layer.py .ima/backups/$DATE/ 2>/dev/null || true


echo "[2/10] Python syntax check"

python3 - <<'PY'
import ast
from pathlib import Path

files=[
    Path("api/server.py"),
    Path("ima_master_runtime.py"),
    Path("identity_context.py"),
    Path("conversation_layer.py")
]

for f in files:
    print("checking",f)
    if not f.exists():
        raise SystemExit("missing "+str(f))
    ast.parse(f.read_text(encoding="utf-8"))

print("ACTIVE CODE SYNTAX OK")
PY


echo "[3/10] Checking core modules"

python3 - <<'PY'
import sys
sys.path.insert(0,'.')

for m in [
    "ima_master_runtime",
    "identity_context",
    "conversation_layer"
]:
    print("importing",m)
    __import__(m)

print("CORE IMPORT OK")
PY


echo "[4/10] Server check"

python3 - <<'PY'
import ast
ast.parse(open("api/server.py").read())
print("SERVER OK")
PY


echo "[5/10] Git status"
git status


echo "[6/10] Git add"
git add .


echo "[7/10] Commit"
git commit -m "IMA stable runtime repair $DATE" || true


echo "[8/10] Tag"
git tag -a "ima-release-$DATE" -m "IMA release $DATE" || true


echo "[9/10] Final check"
git status


echo "[10/10] DONE"
echo "TAG ima-release-$DATE"
