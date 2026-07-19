#!/data/data/com.termux/files/usr/bin/bash
set -u

ROOT="/data/data/com.termux/files/home/ima_kernel"
AUTO="$ROOT/.ima/automation"
LOG="$AUTO/logs/watchdog.log"
LOCK="$AUTO/.watchdog.lock"
SUPERVISOR="$AUTO/supervisor.sh"
INTERVAL="${IMA_WATCHDOG_INTERVAL_SECONDS:-30}"

mkdir -p "$AUTO/logs"

exec 9>"$LOCK"
if ! flock -n 9; then
    echo "$(date -Is) WATCHDOG_ALREADY_RUNNING" >> "$LOG"
    exit 0
fi

cd "$ROOT" || exit 1

echo $$ > "$AUTO/watchdog.pid"

cleanup() {
    rm -f "$AUTO/watchdog.pid"
    echo "$(date -Is) WATCHDOG_STOPPED PID=$$" >> "$LOG"
    exit 0
}

trap cleanup INT TERM EXIT

echo "$(date -Is) WATCHDOG_STARTED PID=$$" >> "$LOG"

while true; do
    if ! pgrep -f '[/]ima/automation/supervisor.sh' >/dev/null 2>&1; then
        echo "$(date -Is) SUPERVISOR_NOT_RUNNING_STARTING" >> "$LOG"
        nohup "$SUPERVISOR" \
            >> "$AUTO/logs/nohup-supervisor.log" 2>&1 &
        sleep 2
    fi

    sleep "$INTERVAL"
done
