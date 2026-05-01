#!/data/data/com.termux/files/usr/bin/bash

LOG=/data/data/com.termux/files/home/ima_core/kernel/server.log

ACTION="$1"

case "$ACTION" in

  restart)
    echo "[EXEC] restart started" | tee -a $LOG

    # מניעת כפילות
    pkill -f prod_server.js || true
    sleep 2

    cd /data/data/com.termux/files/home/ima_core/kernel
    nohup node prod_server.js >> $LOG 2>&1 &

    echo "[EXEC] restart done" | tee -a $LOG
  ;;

esac
