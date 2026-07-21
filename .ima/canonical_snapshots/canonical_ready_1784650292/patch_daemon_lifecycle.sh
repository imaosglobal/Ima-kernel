#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA DAEMON LIFECYCLE PATCH ==="

python3 - <<'PY'
from pathlib import Path

p = Path("ima_daemon.py")
s = p.read_text()

s = s.replace(
'''def run():
    print("[IMA DAEMON] stable brain started")
''',
'''def run():
    print("[IMA DAEMON] stable brain started")

    try:
        emit("KERNEL_BOOT")

        events = load_events()

        if events is not None:
            emit("KERNEL_READY")

    except Exception as e:
        emit("KERNEL_ERROR", text=str(e))
        raise
'''
)

s = s.replace(
'''        except Exception as e:
            emit("ERROR", text=str(e))
            time.sleep(1)
''',
'''        except Exception as e:
            emit("KERNEL_ERROR", text=str(e))
            emit("ERROR", text=str(e))
            time.sleep(1)
'''
)

p.write_text(s)
PY


python3 -m py_compile ima_daemon.py


echo "=== RESTART ==="

pkill -f ima_daemon.py || true

sleep 1

nohup python3 ima_daemon.py > .ima/daemon.log 2>&1 &

sleep 2


echo "=== CHECK EVENTS ==="

tail -20 .ima/ledger.jsonl | grep KERNEL || true


echo "=== CHECK STATE ==="

python3 - <<'PY'
from ima_kernel import load_events
import sys
sys.path.insert(0,'.ima')
from ima_reducer import reduce

print(reduce(load_events()))
PY


git add ima_daemon.py
git commit -m "IMA: daemon lifecycle boot ready error events"
git push origin feature/state-machine

echo "=== DONE ==="
