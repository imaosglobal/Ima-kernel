#!/data/data/com.termux/files/usr/bin/bash

CMD=$1

DECISION=$(node ~/ima_core/kernel/decision_engine.js "$CMD")

ALLOW=$(echo "$DECISION" | grep -o '"decision": *"ALLOW"')

echo "$DECISION"

if [[ -n "$ALLOW" ]]; then
    echo "[GATE] EXECUTING: $CMD"
    bash ~/ima_core/kernel/ima_cli.sh "$CMD"
else
    echo "[GATE] BLOCKED OR DEFERRED: $CMD"
fi
