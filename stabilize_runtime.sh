#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"

echo ""
echo "======================="
echo "IMA RUNTIME STABILIZER"
echo "======================="
echo ""

mkdir -p $ROOT/runtime/logs
mkdir -p $ROOT/runtime/pids
mkdir -p $ROOT/runtime/state
mkdir -p $ROOT/runtime/tmp

echo "[1] killing duplicate node processes..."

pkill -f "_tmp_server.js" 2>/dev/null
pkill -f "server_tmp.js" 2>/dev/null
pkill -f "server_backup.js" 2>/dev/null

sleep 1

echo "[2] cleaning locks..."

rm -f $ROOT/runtime/*.lock
rm -f $ROOT/runtime/server.lock
rm -f $ROOT/runtime/instance.lock

echo "[3] rebuilding main lock..."

echo $$ > $ROOT/runtime/ima.lock

echo "[4] checking memory files..."

for f in \
memory.json \
memory_backup.json \
kernel/cloud/memory.json \
kernel/cloud/state.json
do

  if [ -f "$ROOT/$f" ]; then
    echo "OK => $f"
  else
    echo "{}" > "$ROOT/$f"
    echo "CREATED => $f"
  fi

done

echo "[5] ensuring single server..."

COUNT=$(ps -ef | grep node | grep server.js | grep -v grep | wc -l)

echo "SERVER COUNT => $COUNT"

if [ "$COUNT" -gt 1 ]; then

  echo "DUPLICATE SERVERS DETECTED"

  pkill -f server.js

  sleep 2

  nohup node $ROOT/server.js \
    >> $ROOT/runtime/logs/server.log 2>&1 &

else

  echo "SERVER OK"

fi

echo "[6] watchdog..."

if [ ! -f "$ROOT/watchdog.sh" ]; then

cat > $ROOT/watchdog.sh <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"

while true
do

COUNT=$(ps -ef | grep node | grep server.js | grep -v grep | wc -l)

if [ "$COUNT" -eq 0 ]; then

  echo "[WATCHDOG] restarting server..."

  nohup node $ROOT/server.js \
    >> $ROOT/runtime/logs/server.log 2>&1 &

fi

sleep 15

done
EOF

chmod +x $ROOT/watchdog.sh

fi

echo "[7] starting watchdog..."

pkill -f watchdog.sh 2>/dev/null

nohup bash $ROOT/watchdog.sh \
>> $ROOT/runtime/logs/watchdog.log 2>&1 &

echo ""
echo "SYSTEM STABILIZED"
echo ""
