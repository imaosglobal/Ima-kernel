#!/data/data/com.termux/files/usr/bin/bash
set -u

ROOT="/data/data/com.termux/files/home/ima_kernel"
AUTO="$ROOT/.ima/automation"
LOG="$AUTO/logs/watchdog.log"
LOCK="$AUTO/.watchdog.lock"
PIDFILE="$AUTO/watchdog.pid"
SUPERVISOR="$AUTO/supervisor.sh"
SUP_PIDFILE="$AUTO/supervisor.pid"
INTERVAL="${IMA_WATCHDOG_INTERVAL_SECONDS:-30}"

mkdir -p "$AUTO/logs"

exec 9>"$LOCK"

if ! flock -n 9; then
    echo "$(date -Is) WATCHDOG_ALREADY_RUNNING" >> "$LOG"
    exit 0
fi

cd "$ROOT" || exit 1
echo $$ > "$PIDFILE"

cleanup() {
    if [ -f "$PIDFILE" ] && [ "$(cat "$PIDFILE" 2>/dev/null)" = "$$" ]; then
        rm -f "$PIDFILE"
    fi
    echo "$(date -Is) WATCHDOG_STOPPED PID=$$" >> "$LOG"
    exit 0
}

trap cleanup INT TERM EXIT

echo "$(date -Is) WATCHDOG_STARTED PID=$$" >> "$LOG"

while true; do
    SUP_RUNNING=0

    if [ -f "$SUP_PIDFILE" ]; then
        SUP_PID="$(cat "$SUP_PIDFILE" 2>/dev/null || true)"

        if [ -n "$SUP_PID" ] && kill -0 "$SUP_PID" 2>/dev/null; then
            SUP_RUNNING=1
        fi
    fi

    if [ "$SUP_RUNNING" -eq 0 ]; then
        echo "$(date -Is) SUPERVISOR_NOT_RUNNING_STARTING" >> "$LOG"

        nohup "$SUPERVISOR" \
            >> "$AUTO/logs/nohup-supervisor.log" 2>&1 &

        sleep 3
    fi

    sleep "$INTERVAL"
done
