#!/data/data/com.termux/files/usr/bin/bash
set -u

ROOT="/data/data/com.termux/files/home/ima_kernel"
AUTO="$ROOT/.ima/automation"
LOG="$AUTO/logs/supervisor.log"
LOCK="$AUTO/.supervisor.lock"
PIDFILE="$AUTO/supervisor.pid"
INTERVAL="${IMA_INTERVAL_SECONDS:-300}"

mkdir -p \
  "$AUTO/logs" \
  "$AUTO/metrics" \
  "$AUTO/backups" \
  "$AUTO/feedback" \
  "$AUTO/proposals"

exec 9>"$LOCK"

if ! flock -n 9; then
    echo "$(date -Is) supervisor already running" >> "$LOG"
    exit 0
fi

cd "$ROOT" || exit 1
echo $$ > "$PIDFILE"

cleanup() {
    rm -f "$PIDFILE"
    echo "$(date -Is) SUPERVISOR STOPPED PID=$$" >> "$LOG"
    exit 0
}

trap cleanup INT TERM EXIT

echo "$(date -Is) SUPERVISOR STARTED PID=$$ INTERVAL=${INTERVAL}s" >> "$LOG"

while true; do
    START=$(date +%s)

    if python3 "$AUTO/continuous_improvement_loop.py" \
        >> "$AUTO/logs/continuous_improvement.log" 2>&1
    then
        echo "$(date -Is) CYCLE OK" >> "$LOG"
    else
        CODE=$?
        echo "$(date -Is) CYCLE FAILED code=$CODE" >> "$LOG"
    fi

    END=$(date +%s)
    ELAPSED=$((END - START))
    SLEEP_FOR=$((INTERVAL - ELAPSED))

    [ "$SLEEP_FOR" -lt 10 ] && SLEEP_FOR=10

    echo "$(date -Is) NEXT CYCLE IN ${SLEEP_FOR}s" >> "$LOG"
    sleep "$SLEEP_FOR"
done
