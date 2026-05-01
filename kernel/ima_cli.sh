
#!/data/data/com.termux/files/usr/bin/bash

CMD="$1"

case "$CMD" in
  restart)
    bash ~/ima_core/kernel/ima_gate.sh restart
    ;;
  update)
    bash ~/ima_core/kernel/ima_update.sh
    ;;
  brain)
    node ~/ima_core/kernel/decision_engine.js brain
    ;;
  health)
    ima health
    ;;
  queue)
    ima queue
    ;;
  *)
    echo "[CLI] UNKNOWN COMMAND: $CMD"
    ;;
esac

