#!/data/data/com.termux/files/usr/bin/bash
set -u

PREFIX="/data/data/com.termux/files/usr"
HOME_DIR="/data/data/com.termux/files/home"
ROOT="$HOME_DIR/Ima-kernel"
BRIDGE_DIR="$ROOT/tools/termux-ima-bridge"
LOG="$HOME_DIR/.config/ima/bridge-autostart.log"
mkdir -p "$(dirname "$LOG")"
exec >>"$LOG" 2>&1

echo "=== $(date -Is) IMA bridge autostart ==="

export PATH="$PREFIX/bin:$PATH"
export IMA_CHROME_CDP="http://127.0.0.1:9222"
export IMA_CHROME_TARGET_HINT="imaosglobal.github.io/Ima-kernel"

# Do not create a duplicate bridge.
if pgrep -f "$BRIDGE_DIR/bridge.py" >/dev/null 2>&1; then
  echo "bridge already running"
  exit 0
fi

# Wake Chrome and ensure the canonical IMA target exists.
"$PREFIX/bin/am" start -a android.intent.action.VIEW -d "https://imaosglobal.github.io/Ima-kernel/" com.android.chrome >/dev/null 2>&1 || true

# Start exactly one canonical bridge in the background.
cd "$BRIDGE_DIR"
"$PREFIX/bin/python" bridge.py &
BRIDGE_PID=$!

# Keep the bridge connected if Android restores the already-paired ADB
# transport after boot. No manual port forwarding is then needed.
while kill -0 "$BRIDGE_PID" 2>/dev/null; do
  SERIAL=$("$PREFIX/bin/adb" devices 2>/dev/null | awk 'NR>1 && $2=="device" {print $1; exit}')
  if [ -n "${SERIAL:-}" ]; then
    "$PREFIX/bin/adb" -s "$SERIAL" forward --remove tcp:9222 >/dev/null 2>&1 || true
    "$PREFIX/bin/adb" -s "$SERIAL" forward tcp:9222 localabstract:chrome_devtools_remote >/dev/null 2>&1 || true
  fi
  sleep 5
done

echo "bridge exited; autostart loop ending"
