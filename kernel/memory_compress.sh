#!/data/data/com.termux/files/usr/bin/bash

set -e

BASE="$HOME/ima_kernel/kernel/cloud"

MEM="$BASE/memory.json"
ARCH="$BASE/memory_archive.json"

echo "[IMA COMPRESS] starting..."

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

# אם יש יותר מ־50 זיכרונות → דחיסה
if len(items) > 50:
    old = items[:-20]   # שומרים רק 20 אחרונים
    recent = items[-20:]

    # יצירת סיכום דחוס
    summary = {
        "compressed_count": len(old),
        "summary_text": " | ".join([str(i.get("entry",""))[:50] for i in old[:10]])
    }

    arch.setdefault("archive", []).append(summary)

    mem["memory"] = recent

    json.dump(mem, open(MEM,"w"), indent=2)
    json.dump(arch, open(ARCH,"w"), indent=2)

    print("[OK] compressed:", len(old))
else:
    print("[SKIP] not enough data")

PY

echo "[DONE] compression cycle complete"
