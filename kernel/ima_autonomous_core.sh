#!/data/data/com.termux/files/usr/bin/bash
set -e

BASE="$HOME/ima_kernel/kernel/cloud"

MEM="$BASE/memory.json"
ARCH="$BASE/memory_archive.json"
INDEX="$BASE/memory_index.json"
SUMMARY="$BASE/memory_summary.json"

mkdir -p "$BASE"

echo "===== IMA AUTONOMOUS CORE ====="

# ---------------- BOOTSTRAP ----------------
echo "[BOOT] ensuring system baseline..."

[ -f "$MEM" ] || echo '{"memory":[]}' > "$MEM"
[ -f "$ARCH" ] || echo '{"archive":[]}' > "$ARCH"

# ---------------- HEALTH CHECK ----------------
echo "[HEALTH]"
curl -s http://127.0.0.1:3000/health || echo "[WARN] server down"

pgrep -f server.js >/dev/null || {
  echo "[RECOVER] restarting server..."
  nohup node ~/ima_kernel/server.js > ~/ima_kernel/runtime/logs/server.log 2>&1 &
}

pgrep -f watchdog.sh >/dev/null || {
  echo "[RECOVER] restarting watchdog..."
  nohup bash ~/ima_kernel/watchdog.sh > ~/ima_kernel/runtime/logs/watchdog.log 2>&1 &
}

# ---------------- INDEX REBUILD ----------------
echo "[INDEX] rebuilding..."

python3 - << 'PY'
import json, os

BASE=os.path.expanduser("~/ima_kernel/kernel/cloud")

MEM=os.path.join(BASE,"memory.json")
ARCH=os.path.join(BASE,"memory_archive.json")
INDEX=os.path.join(BASE,"memory_index.json")
SUMMARY=os.path.join(BASE,"memory_summary.json")

def load(p):
    try:
        return json.load(open(p))
    except:
        return {"memory":[]}

mem=load(MEM)
arch=load(ARCH)

items=mem.get("memory",[])+arch.get("archive",[])

# bootstrap fix if empty
if not items:
    items=[{"entry":"bootstrap system","type":"system"}]

index={}
for i,x in enumerate(items):
    for w in str(x.get("entry","")).lower().split():
        index.setdefault(w,[]).append(i)

summary={
    "total_entries":len(items),
    "types":{}
}

for x in items:
    t=x.get("type","unknown")
    summary["types"][t]=summary["types"].get(t,0)+1

json.dump(index,open(INDEX,"w"),indent=2)
json.dump(summary,open(SUMMARY,"w"),indent=2)

print("[OK] index + summary synced")
PY

# ---------------- COMPRESSION ----------------
echo "[COMPRESS] checking..."

python3 - << 'PY'
import json, os

BASE=os.path.expanduser("~/ima_kernel/kernel/cloud")

MEM=os.path.join(BASE,"memory.json")
ARCH=os.path.join(BASE,"memory_archive.json")

def load(p):
    try:
        return json.load(open(p))
    except:
        return {"memory":[]}

mem=load(MEM)
arch=load(ARCH)

items=mem.get("memory",[])

if len(items)>80:
    old=items[:-40]
    recent=items[-40:]

    block={
        "type":"auto_compression",
        "count":len(old),
        "sample":" | ".join([str(x.get("entry",""))[:40] for x in old[:10]])
    }

    arch.setdefault("archive",[]).append(block)
    mem["memory"]=recent

    json.dump(mem,open(MEM,"w"),indent=2)
    json.dump(arch,open(ARCH,"w"),indent=2)

    print("[OK] compressed",len(old))
else:
    print("[SKIP] compression")
PY

# ---------------- SELF CHECK ----------------
echo "[AUDIT]"
echo "files:" $(find "$BASE" -type f | wc -l)

echo "[DONE] autonomous cycle complete"
