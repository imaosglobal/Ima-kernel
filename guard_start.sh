#!/data/data/com.termux/files/usr/bin/bash

if pgrep -f "server.js" > /dev/null; then
  exit 0
fi

cd "$HOME/ima_kernel"
nohup node server.js > runtime/logs/server.log 2>&1 &
