#!/data/data/com.termux/files/usr/bin/bash

set -e

BASE="$HOME/ima_kernel/kernel/cloud"

MEM="$BASE/memory.json"
ARCH="$BASE/memory_archive.json"
INDEX="$BASE/memory_index.json"
SUMMARY="$BASE/memory_summary.json"

mkdir -p "$BASE"

echo "[IMA ENGINE] starting pipeline..."

# ---------- load safe ----------
python3 - << 'PY'
import json, os

BASE = os.path.expanduser("~/ima_kernel/kernel/cloud")

MEM = os.path.join(BASE, "memory.json")
ARCH = os.path.join(BASE, "memory_archive.json")
INDEX = os.path.join(BASE, "memory_index.json")
SUMMARY = os.path.join(BASE, "memory_summary.json")

def load(path, fallback):
    try:
        return json.load(open(path))
    except:
        return fallback

mem = load(MEM, {"memory":[]})
arch = load(ARCH, {"archive":[]})

items = mem.get("memory", []) + arch.get("archive", [])

# ---------- INDEX ----------
index = {}
for i, item in enumerate(items):
    text = str(item.get("entry","")).lower()
    for w in text.split():
        w = w.strip()
        if w:
            index.setdefault(w, []).append(i)

# ---------- SUMMARY ----------
summary = {
    "total_entries": len(items),
    "last_entry": items[-1] if items else None,
    "types": {}
}

for item in items:
    t = item.get("type","unknown")
    summary["types"][t] = summary["types"].get(t,0) + 1

# ---------- WRITE ----------
json.dump(index, open(INDEX,"w"), indent=2, ensure_ascii=False)
json.dump(summary, open(SUMMARY,"w"), indent=2, ensure_ascii=False)

print("[OK] index + summary rebuilt")
PY

# ---------- COMPRESSION ----------
echo "[IMA ENGINE] checking compression..."

python3 - << 'PY'
import json, os

BASE = os.path.expanduser("~/ima_kernel/kernel/cloud")

MEM = os.path.join(BASE, "memory.json")
ARCH = os.path.join(BASE, "memory_archive.json")

def load(path):
    try:
        return json.load(open(path))
    except:
        return {"memory":[]}

mem = load(MEM)
arch = load(ARCH)

items = mem.get("memory", [])

if len(items) > 60:
    old = items[:-30]
    recent = items[-30:]

    summary_block = {
        "type": "compressed_memory",
        "compressed_count": len(old),
        "summary": " | ".join([str(i.get("entry",""))[:40] for i in old[:10]])
    }

    arch.setdefault("archive", []).append(summary_block)
    mem["memory"] = recent

    json.dump(mem, open(MEM,"w"), indent=2)
    json.dump(arch, open(ARCH,"w"), indent=2)

    print("[OK] compressed:", len(old))
else:
    print("[SKIP] compression not needed")
PY

# ---------- HEALTH CHECK ----------
echo "[IMA ENGINE] health check:"
curl -s http://127.0.0.1:3000/health || echo "[WARN] server down"

# ---------- VERIFY FILES ----------
echo "[IMA ENGINE] verifying layers..."

[ -f "$MEM" ] && echo "memory OK" || echo "memory MISSING"
[ -f "$INDEX" ] && echo "index OK" || echo "index MISSING"
[ -f "$SUMMARY" ] && echo "summary OK" || echo "summary MISSING"
[ -f "$ARCH" ] && echo "archive OK" || echo "archive MISSING"

echo "[IMA ENGINE] DONE"
