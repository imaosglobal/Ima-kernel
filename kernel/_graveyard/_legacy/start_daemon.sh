
#!/data/data/com.termux/files/usr/bin/bash

LOCK=~/ima_core/kernel/runtime/daemon.lock
LOG=~/ima_core/kernel/daemon.log

mkdir -p ~/ima_core/kernel/runtime

# אם PID קיים וחי → אל תפעיל חדש
if [ -f "$LOCK" ]; then
  OLD_PID=$(cat $LOCK)

  if kill -0 $OLD_PID 2>/dev/null; then
    echo "[DAEMON] already running ($OLD_PID)"
    exit 0
  fi
fi

cd ~/ima_core/kernel

echo "[DAEMON] starting..." >> $LOG

node control_daemon.js >> $LOG 2>&1 &
PID=$!

echo $PID > $LOCK
echo $PID > ~/ima_core/kernel/.daemon_pid

echo "[DAEMON] PID $PID started" >> $LOG

