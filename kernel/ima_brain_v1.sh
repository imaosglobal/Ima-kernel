#!/data/data/com.termux/files/usr/bin/bash

BASE=~/ima_kernel/kernel/cloud

MEM=$BASE/memory.json
ARCH=$BASE/memory_archive.json
INDEX=$BASE/memory_index.json
SUMMARY=$BASE/memory_summary.json

CMD="$1"
QUERY="$2"

mkdir -p $BASE

ask() {
  python3 - << PY
import json,os

mem=json.load(open("$MEM")) if os.path.exists("$MEM") else {"memory":[]}

q="$QUERY".lower()

hits=[]
for i,item in enumerate(mem.get("memory",[])):
    if q in str(item.get("entry","")).lower():
        hits.append(item)

print(json.dumps({
    "query":"$QUERY",
    "results":hits[:5],
    "count":len(hits)
}, indent=2, ensure_ascii=False))
PY
}

act() {
  echo "[AGENT] executing action: $QUERY"

  case "$QUERY" in
    "health")
      curl -s http://127.0.0.1:3000/health
      ;;
    "restart")
      pkill -f server.js || true
      nohup node ~/ima_kernel/server.js > ~/ima_kernel/runtime/logs/server.log 2>&1 &
      echo "restarted"
      ;;
    *)
      echo "unknown action"
      ;;
  esac
}

route() {
  case "$CMD" in

    ask)
      echo "[BRAIN] knowledge layer"
      ask
      ;;

    act)
      echo "[BRAIN] agent layer"
      act
      ;;

    hybrid)
      echo "[BRAIN] split mode"
      ask
      act
      ;;

    *)
      echo "usage: ask | act | hybrid"
      ;;
  esac
}

route
