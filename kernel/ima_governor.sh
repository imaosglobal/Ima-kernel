
#!/data/data/com.termux/files/usr/bin/bash

ACTION=$1
shift

RESULT=$(node ~/ima_core/kernel/decision_engine.js "$ACTION")

DECISION=$(echo "$RESULT" | grep -o '"decision": *"[^"]*"' | cut -d'"' -f4)

echo "$RESULT"

if [ "$DECISION" = "BLOCK" ]; then
  echo "[GOVERNOR] ACTION BLOCKED"
  exit 1
fi

if [ "$DECISION" = "DEFER" ]; then
  echo "[GOVERNOR] ACTION DEFERRED - retry later"
  exit 2
fi

echo "[GOVERNOR] ACTION ALLOWED"

# כאן נבצע את הפעולה בפועל
case "$ACTION" in
  restart)
    ima restart
    ;;
  update)
    ima update
    ;;
  brain)
    ima brain
    ;;
  health)
    ima health
    ;;
  queue)
    ima queue
    ;;
  *)
    echo "[GOVERNOR] unknown action"
    ;;
esac

