#!/data/data/com.termux/files/usr/bin/bash
set -u

ROOT="/data/data/com.termux/files/home/ima_kernel"
AUTO="$ROOT/.ima/automation"
LOG="$AUTO/logs/watchdog.log"
LOCK="$AUTO/.watchdog.lock"
PIDFILE="$AUTO/watchdog.pid"
SUPERVISOR="$AUTO/supervisor.sh"
INTERVAL="${IMA_WATCHDOG_INTERVAL_SECONDS:-30}"

mkdir -p "$AUTO/logs"

exec 9>"$LOCK"
if ! flock -n 9; then
    exit 0
fi

cd "$ROOT" || exit 1
echo "$$" > "$PIDFILE"

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
    SUP_PID=""

    while read -r PID ARGS; do
        case "$ARGS" in
            */.ima/automation/supervisor.sh*)
                SUP_PID="$PID"
                break
                ;;
        esac
    done < <(ps -eo pid=,args=)

    if [ -n "$SUP_PID" ] && kill -0 "$SUP_PID" 2>/dev/null; then
        if [ ! -f "$AUTO/supervisor.pid" ] || [ "$(cat "$AUTO/supervisor.pid" 2>/dev/null)" != "$SUP_PID" ]; then
            echo "$SUP_PID" > "$AUTO/supervisor.pid"
            echo "$(date -Is) SUPERVISOR_PIDFILE_REPAIRED PID=$SUP_PID" >> "$LOG"
        fi
    else
        echo "$(date -Is) SUPERVISOR_NOT_RUNNING_STARTING" >> "$LOG"

        nohup "$SUPERVISOR" \
            >> "$AUTO/logs/nohup-supervisor.log" 2>&1 &

        sleep 3

        while read -r PID ARGS; do
            case "$ARGS" in
                */.ima/automation/supervisor.sh*)
                    SUP_PID="$PID"
                    break
                    ;;
            esac
        done < <(ps -eo pid=,args=)

        if [ -n "$SUP_PID" ] && kill -0 "$SUP_PID" 2>/dev/null; then
            echo "$SUP_PID" > "$AUTO/supervisor.pid"
            echo "$(date -Is) SUPERVISOR_STARTED PID=$SUP_PID" >> "$LOG"
        else
            echo "$(date -Is) SUPERVISOR_START_FAILED" >> "$LOG"
        fi
    fi

    sleep "$INTERVAL"
done
