#!/data/data/com.termux/files/usr/bin/bash
set +e
cd "$(dirname "$0")"
if [ -f .ima/deal_hunter.pid ]; then
  kill "$(cat .ima/deal_hunter.pid)" 2>/dev/null || true
  rm -f .ima/deal_hunter.pid
fi
echo "DEAL_HUNTER_STOPPED"
