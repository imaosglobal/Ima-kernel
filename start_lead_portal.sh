#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")"
export PYTHONPATH="$PWD:${PYTHONPATH:-}"
mkdir -p .ima
if [ -f .ima/lead_portal.pid ]; then kill "$(cat .ima/lead_portal.pid)" 2>/dev/null || true; fi
nohup python -m founder.executive_ai.global_intelligence.lead_portal >> .ima/lead_portal.log 2>&1 &
echo $! > .ima/lead_portal.pid
echo "LEAD_PORTAL_STARTED pid=$(cat .ima/lead_portal.pid) bind=0.0.0.0:8765"
