#!/data/data/com.termux/files/usr/bin/bash

case "$1" in
    restart)
        echo "[CLI] RESTART APPROVED"
        bash ~/ima_core/kernel/executor.sh restart
        echo "[CLI] RESTART EXECUTED"
    ;;
    update)
        bash ~/ima_core/kernel/update_engine.sh
    ;;
    brain)
        node ~/ima_core/kernel/control_brain.js
    ;;
    health)
        curl -s http://localhost:4000/health
    ;;
    queue)
        curl -s http://localhost:4000/v2/queue
    ;;
    -h|--help|help|*)
        echo "ima: restart | update | brain | health | queue"
    ;;
esac
