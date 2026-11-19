#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
pkg update
pkg install -y python
python -m pip install websocket-client
echo 'IMA Termux bridge tools installed.'
echo 'LIVE-001 uses the outbound native Android transport; Wireless Debugging is not required.'
echo 'Canonical launcher: python ~/Ima-kernel/tools/termux-ima-bridge/bridge_launcher.py'
