#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$HOME/ima_kernel"
while true; do
  python .ima/ORCHESTRATION/ima_orchestrator_entry.py \
    >> .ima/ORCHESTRATION/logs/supervisor.log 2>&1 || true
  sleep 300
done
