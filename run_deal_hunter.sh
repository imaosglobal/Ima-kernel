#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")"
export PYTHONPATH="$PWD:${PYTHONPATH:-}"
exec python -m founder.executive_ai.global_intelligence.deal_hunter
