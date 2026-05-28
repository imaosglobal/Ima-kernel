#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"

pkill -f guardian_daemon.sh 2>/dev/null

nohup bash $ROOT/guardian_daemon.sh \
>> $ROOT/runtime/logs/guardian.log 2>&1 &

echo "GUARDIAN ACTIVE"
