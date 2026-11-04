#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
pkg update
pkg install -y git python nodejs android-tools golang
python -m pip install --upgrade pip
python -m pip install websocket-client
if [ ! -d "$HOME/mobilebridge" ]; then git clone https://github.com/VulpineOS/mobilebridge.git "$HOME/mobilebridge"; fi
cd "$HOME/mobilebridge"
go install ./cmd/mobilebridge
echo 'IMA Termux bridge tools installed.'
echo 'Pair/connect Wireless debugging, then run: mobilebridge --port 9222'
echo 'Then run: python ~/Ima-kernel/tools/termux-ima-bridge/bridge.py'