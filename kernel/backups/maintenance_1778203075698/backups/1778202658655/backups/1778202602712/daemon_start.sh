#!/data/data/com.termux/files/usr/bin/bash

echo "=== IMA DAEMON MODE START ==="

cd ~/ima_core/kernel || exit 1

# env load
if [ -f "$HOME/.env" ]; then
  export $(grep -v '^#' $HOME/.env | xargs)
fi

# prevent duplicate daemon
if [ -f daemon.pid ]; then
  OLD_PID=$(cat daemon.pid)
  kill -0 $OLD_PID 2>/dev/null && {
    echo "DAEMON ALREADY RUNNING: $OLD_PID"
    exit 0
  }
fi

# start daemon in background
nohup node ima_daemon.js > daemon.out 2>&1 &

echo $! > daemon.pid

echo "DAEMON STARTED PID: $(cat daemon.pid)"
