
#!/data/data/com.termux/files/usr/bin/bash

ACTION=$1

RESULT=$(node ~/ima_core/kernel/decision_engine.js "$ACTION")

echo "$RESULT"

DECISION=$(echo "$RESULT" | jq -r '.decision')

if [ "$DECISION" = "ALLOW" ]; then
  echo "[GATE] EXECUTING ACTION: $ACTION"
elif [ "$DECISION" = "DEFER" ]; then
  echo "[GATE] DEFERRED: $ACTION"
else
  echo "[GATE] BLOCKED: $ACTION"
fi

