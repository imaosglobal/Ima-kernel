#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== CONNECT IMA_START TO CANONICAL RUNTIME ==="

BACKUP=".ima/backup_IMA_START_$(date +%s)"
mkdir -p "$BACKUP"

cp IMA_START.py "$BACKUP/IMA_START.py"

echo "[OK] IMA_START backup created"

python3 - <<'PY'
from pathlib import Path

p=Path("IMA_START.py")
s=p.read_text()

if "python_bridge" not in s:

    s=s.replace(
        "import sys",
        "import sys\n\nRUNTIME = ROOT / \"kernel\" / \"runtime\" / \"CANONICAL\"\n"
        "sys.path.insert(0, str(RUNTIME))"
    )

    s=s.replace(
        "def run():",
        """
def check_runtime():
    try:
        from python_bridge import boot_runtime
        result = boot_runtime()

        ok = result.get("status") == "ONLINE"

        status(
            "CANONICAL RUNTIME",
            ok,
            str(result)
        )

        return ok

    except Exception as e:
        status(
            "CANONICAL RUNTIME",
            False,
            str(e)
        )
        return False


def run():
"""
    )

    s=s.replace(
        "results = [",
        "results = [\n"
        "        check_runtime(),"
    )

    p.write_text(s)

    print("[OK] IMA_START patched")

else:
    print("[SKIP] already connected")

PY


echo ""
echo "=== VERIFY IMA_START ==="

python3 IMA_START.py

echo ""
echo "=== COMPLETE ==="
echo "IMA START -> CANONICAL RUNTIME CONNECTED"
