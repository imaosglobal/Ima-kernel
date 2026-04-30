pkill -f prod_server.js || true
sleep 1
nohup node ~/ima_core/kernel/prod_server.js > server.log 2>&1 &
