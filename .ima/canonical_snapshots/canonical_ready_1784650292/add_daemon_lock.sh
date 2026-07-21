#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA DAEMON LOCK PATCH ==="

python3 - <<'PY'
from pathlib import Path

p = Path("ima_daemon.py")
s = p.read_text()

# הוספת imports
s = s.replace(
    "import time",
    "import time\nimport os\nimport atexit\n"
)

# הוספת lock אחרי imports
marker = "seen = set()"

lock_code = '''
LOCK_FILE = ".ima/daemon.lock"

def acquire_lock():
    os.makedirs(".ima", exist_ok=True)

    if os.path.exists(LOCK_FILE):
        print("[IMA DAEMON] already running")
        raise SystemExit(1)

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

    atexit.register(release_lock)


def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

'''

if "def acquire_lock" not in s:
    s = s.replace(marker, lock_code + "\n" + marker)

# להפעיל lock בתחילת run
s = s.replace(
    'def run():\n    print("[IMA DAEMON] stable brain started")',
    'def run():\n    acquire_lock()\n    print("[IMA DAEMON] stable brain started")'
)

p.write_text(s)
PY

python3 -m py_compile ima_daemon.py

echo "[OK] daemon lock added"

git add ima_daemon.py
git commit -m "IMA: add daemon lock protection"

echo "=== DONE ==="
