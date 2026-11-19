#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
pkg update
pkg install -y git python nodejs android-tools golang
python -m pip install websocket-client
echo 'IMA Termux bridge tools installed.'
echo 'No Wireless Debugging pairing is required by the IMA cloud transport.'
echo 'The canonical launcher is: python ~/Ima-kernel/tools/termux-ima-bridge/bridge_launcher.py'
echo 'ADB is legacy/local fallback only; the bridge must not depend on a fixed Wi-Fi address.'