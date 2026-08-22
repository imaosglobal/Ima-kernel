#!/data/data/com.termux/files/usr/bin/bash
cd ~/ima_kernel

echo "=== IMA DIAGNOSTIC ==="

echo "[EVENT FILES]"
find . -type f -name "*.jsonl" -o -name "*.json"

echo
echo "[EVENT COUNT]"
python3 - <<'PY'
from ima_system import load_events
events = load_events()
for e in events[-10:]:
PY

echo
echo "[ASK TEST]"
python3 ima.py ask "מי אתה ומה מצבך?"

echo
echo "[DAEMON LOG]"
cat .ima/daemon.out 2>/dev/null || true

echo
echo "=== END ==="
