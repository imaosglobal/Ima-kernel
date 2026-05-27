#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/ima_kernel/kernel/cloud"

MEM="$BASE/memory.json"
ARCH="$BASE/memory_archive.json"
INDEX="$BASE/memory_index.json"
SUMMARY="$BASE/memory_summary.json"

echo "===== IMA SELF AUDIT ====="

# ---------- FILE COUNT ----------
echo "[1] FILE SYSTEM CHECK"
FILE_COUNT=$(find "$BASE" -type f | wc -l)
echo "files in memory system: $FILE_COUNT"

# ---------- MEMORY VALIDITY ----------
echo "[2] MEMORY VALIDATION"
if python3 - << PY
import json, os
try:
    data = json.load(open("$MEM"))
    print("memory OK, entries:", len(data.get("memory",[])))
except:
    print("memory BROKEN")
PY
then
    echo ""
fi

# ---------- INDEX CHECK ----------
echo "[3] INDEX CHECK"
if [ -f "$INDEX" ]; then
  echo "index exists"
  python3 - << PY
import json
try:
    d=json.load(open("$INDEX"))
    print("index keys:", len(d))
except:
    print("index broken")
PY
else
  echo "index MISSING"
fi

# ---------- SUMMARY CHECK ----------
echo "[4] SUMMARY CHECK"
if [ -f "$SUMMARY" ]; then
  python3 - << PY
import json
try:
    d=json.load(open("$SUMMARY"))
    print("total entries:", d.get("total_entries"))
except:
    print("summary broken")
PY
else
  echo "summary MISSING"
fi

# ---------- ARCHIVE CHECK ----------
echo "[5] ARCHIVE CHECK"
if [ -f "$ARCH" ]; then
  python3 - << PY
import json
try:
    d=json.load(open("$ARCH"))
    print("archive blocks:", len(d.get("archive",[])))
except:
    print("archive broken")
PY
else
  echo "archive MISSING"
fi

# ---------- SERVER CHECK ----------
echo "[6] SERVER CHECK"
curl -s http://127.0.0.1:3000/health || echo "SERVER DOWN"

# ---------- WATCHDOG CHECK ----------
echo "[7] PROCESS CHECK"
pgrep -af server.js || echo "server not running"
pgrep -af watchdog.sh || echo "watchdog not running"

echo "===== AUDIT COMPLETE ====="
