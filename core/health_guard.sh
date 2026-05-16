#!/data/data/com.termux/files/usr/bin/bash

NODE_OK=$(command -v node >/dev/null 2>&1 && echo 1 || echo 0)
NPM_OK=$(command -v npm >/dev/null 2>&1 && echo 1 || echo 0)
PORT_OK=$(curl -s localhost:3000/health >/dev/null && echo 1 || echo 0)

if [ "$NODE_OK" -eq 1 ] && [ "$NPM_OK" -eq 1 ] && [ "$PORT_OK" -eq 1 ]; then
  echo '{"health":"OK","mode":"FINAL_SINGLE_SYSTEM"}'
  exit 0
fi

echo '{"health":"RECOVERING"}'

# auto-heal
pkill -f node
cd ~/ima_kernel && ./scripts/start.sh
