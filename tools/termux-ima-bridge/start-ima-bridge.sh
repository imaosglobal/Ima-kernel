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
export IMA_MCP_URL="https://ima-universal-action-core.onrender.com/mcp"
export IMA_ANDROID_DOWNLOADS="$HOME_DIR/storage/downloads"

# Keep one canonical bridge process; the launcher extends bridge.py with MCP relay endpoints.
if pgrep -f "$BRIDGE_DIR/bridge_launcher.py" >/dev/null 2>&1 || pgrep -f "$BRIDGE_DIR/bridge.py" >/dev/null 2>&1; then
  echo "bridge already running"
  exit 0
fi

"$PREFIX/bin/am" start -a android.intent.action.VIEW -d "https://imaosglobal.github.io/Ima-kernel/" com.android.chrome >/dev/null 2>&1 || true

cd "$BRIDGE_DIR"
"$PREFIX/bin/python" bridge_launcher.py &
BRIDGE_PID=$!

wait "$BRIDGE_PID"
echo "bridge exited; autostart loop ending"
