#!/data/data/com.termux/files/usr/bin/bash
set -u
echo "=== IMA TERMUX BRIDGE QA ==="
echo "--- Python ---"
command -v python3 || command -v python || true
python3 --version 2>&1 || true

echo "--- ADB ---"
command -v adb || true
adb devices 2>&1 || true

echo "--- Chrome CDP ---"
curl -fsS --max-time 5 http://127.0.0.1:9222/json/version 2>&1 | head -c 1200 || true
echo

echo "--- Chrome targets ---"
curl -fsS --max-time 5 http://127.0.0.1:9222/json/list 2>&1 | head -c 3000 || true
echo

echo "--- IMA bridge process ---"
ps -ef 2>/dev/null | grep '[t]ermux-ima-bridge/bridge.py' || true

echo "--- IMA bridge status ---"
curl -fsS --max-time 5 http://127.0.0.1:8787/status 2>&1 | head -c 2500 || true
echo

echo "--- Cloud runtime reachability ---"
curl -fsS --max-time 12 https://ima-915m.onrender.com/ima-api/runtime 2>&1 | head -c 2500 || true
echo

echo "--- Device key permissions ---"
if [ -f "$HOME/.config/ima/device.json" ]; then
  ls -l "$HOME/.config/ima/device.json"
  python3 - <<'PY'
import json, pathlib
p=pathlib.Path.home()/'.config/ima/device.json'
try:
    d=json.loads(p.read_text())
    print("device_key_present:", bool(d.get("device_key")))
    print("device_id_present:", bool(d.get("device_id")))
except Exception as e:
    print("device_state_error:", e)
PY
else
  echo "device.json: not enrolled yet"
fi

echo "=== END ==="
