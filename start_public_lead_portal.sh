#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")"
export PYTHONPATH="$PWD:${PYTHONPATH:-}"
if ! command -v cloudflared >/dev/null 2>&1; then
  echo "CLOUDFLARED_MISSING"
  echo "Install it in Termux with: pkg install cloudflared"
  exit 1
fi
if ! curl -fsS http://127.0.0.1:8765 >/dev/null; then
  echo "LEAD_PORTAL_NOT_RUNNING"
  echo "Run: ./start_lead_portal.sh"
  exit 1
fi
mkdir -p .ima
nohup cloudflared tunnel --url http://127.0.0.1:8765 --no-autoupdate > .ima/public_lead_tunnel.log 2>&1 &
echo $! > .ima/public_lead_tunnel.pid
echo "PUBLIC_LEAD_TUNNEL_STARTED pid=$(cat .ima/public_lead_tunnel.pid)"
echo "URL will appear in .ima/public_lead_tunnel.log"
