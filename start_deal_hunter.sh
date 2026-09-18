#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")"
export PYTHONPATH="$PWD:${PYTHONPATH:-}"
mkdir -p .ima
if [ -f .ima/deal_hunter.pid ]; then
  old="$(cat .ima/deal_hunter.pid 2>/dev/null || true)"
  [ -n "$old" ] && kill "$old" 2>/dev/null || true
fi
nohup python -m founder.executive_ai.global_intelligence.deal_hunter_daemon >> .ima/deal_hunter.stdout 2>&1 &
echo $! > .ima/deal_hunter.pid
echo "DEAL_HUNTER_STARTED pid=$(cat .ima/deal_hunter.pid) interval=900s mode=autonomous-discovery+graph+matching+referral-queue+proof-gated-payout"
