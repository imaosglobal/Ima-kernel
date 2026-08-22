#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== IMA ARCHITECTURE AUDIT ==="

echo
echo "[1] ENTRY POINTS"
find . -maxdepth 4 -type f \
\( -name "main.py" -o -name "run.py" -o -name "*boot*.py" -o -name "*start*.py" -o -name "*entry*.py" \) \
| sort

echo
echo "[2] ORCHESTRATORS"
find learning kernel -type f \
-iname "*orchestrator*" 2>/dev/null | sort

echo
echo "[3] BRAIN REFERENCES"
grep -R "brain\|Brain" learning kernel \
-n --include="*.py" 2>/dev/null | head -100

echo
echo "[4] RUNTIME COMPONENTS"
find learning kernel -type f \
-iname "*runtime*" 2>/dev/null | sort

echo
echo "[5] REGISTRIES"
find .ima -type f \
-iname "*registry*" -o -iname "*lock*" 2>/dev/null | sort

echo
echo "[6] PYTHON MODULE HEALTH"

python3 - <<'PY'
from pathlib import Path
import importlib

mods=[]

for p in Path("learning").glob("*.py"):
    if p.name.startswith("_"):
        continue
    mods.append("learning."+p.stem)

ok=[]
bad=[]

for m in mods:
    try:
        importlib.import_module(m)
        ok.append(m)
    except Exception as e:
        bad.append((m,str(e)))

for x in ok:

for x,e in bad:
PY

echo
echo "[7] DUPLICATE FILE NAMES"

find learning kernel -type f \
| sed 's#.*/##' \
| sort \
| uniq -d

echo
echo "[8] CANONICAL BRAIN CHECK"

python3 - <<'PY'
from learning.brain_guard import verify_brain

verify_brain("learning/meta_orchestrator.py")

PY

echo
echo "[9] FULL SYSTEM CHECK"

if [ -f ima_full_system_check.py ]; then
    python3 ima_full_system_check.py
fi

echo
echo "=== AUDIT COMPLETE ==="

