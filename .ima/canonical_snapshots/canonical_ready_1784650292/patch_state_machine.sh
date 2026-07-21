#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA STATE MACHINE PATCH ==="

python3 - <<'PY'
from pathlib import Path

p = Path(".ima/ima_reducer.py")
s = p.read_text()

s = s.replace(
'''        elif t == "KERNEL_REBUILD":
            state["mode"] = "REBUILT"
''',
'''        elif t == "KERNEL_BOOT":
            state["mode"] = "BOOTING"

        elif t == "KERNEL_READY":
            state["mode"] = "READY"

        elif t == "KERNEL_ERROR":
            state["mode"] = "ERROR"

        elif t == "KERNEL_REBUILD":
            state["mode"] = "REBUILT"
'''
)

p.write_text(s)
PY


python3 - <<'PY'
from pathlib import Path

p = Path("ima_system.py")
s = p.read_text()

if "def boot_event" not in s:
    insert = '''

def boot_event():
    emit("KERNEL_BOOT")


def ready_event():
    emit("KERNEL_READY")

'''
    s += insert

p.write_text(s)
PY


python3 -m py_compile .ima/ima_reducer.py ima_system.py

echo "=== TEST EVENTS ==="

python3 - <<'PY'
from ima_system import emit

emit("KERNEL_BOOT")
emit("KERNEL_READY")
print("events injected")
PY


python3 - <<'PY'
from ima_kernel import load_events
import sys
sys.path.insert(0,'.ima')
from ima_reducer import reduce

state = reduce(load_events())

print(state)
PY

git add .ima/ima_reducer.py ima_system.py
git commit -m "IMA: add kernel lifecycle state machine"
git push origin feature/state-machine

echo "=== DONE ==="
