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

# Reuse an existing ADB transport when available.
"$PREFIX/bin/adb" devices 2>/dev/null | awk 'NR>1 && $2=="device" {print $1; exit}' | {
  read -r SERIAL || true
  if [ -n "${SERIAL:-}" ]; then
    echo "ADB transport: $SERIAL"
    "$PREFIX/bin/adb" -s "$SERIAL" forward --remove tcp:9222 >/dev/null 2>&1 || true
    "$PREFIX/bin/adb" -s "$SERIAL" forward tcp:9222 localabstract:chrome_devtools_remote >/dev/null 2>&1 || true
  else
    echo "No existing ADB transport; keeping bridge dormant until CDP is available."
  fi
}

# Start exactly one canonical bridge. It will expose the cloud polling agent
# when the persisted IMA device key exists.
cd "$BRIDGE_DIR"
exec "$PREFIX/bin/python" bridge.py
