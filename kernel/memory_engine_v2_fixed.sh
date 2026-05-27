#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/ima_kernel"
MEM="$BASE/kernel/cloud/memory.json"
ARCH="$BASE/kernel/cloud/memory_archive.json"
INDEX="$BASE/kernel/cloud/memory_index.json"
SUMMARY="$BASE/kernel/cloud/memory_summary.json"

mkdir -p "$BASE/kernel/cloud"

echo "[IMA V2 FIX] running full rebuild..."

# ---------------- SAFE LOAD ----------------
[ ! -f "$MEM" ] && echo '{"history":[]}' > "$MEM"

# ---------------- PYTHON PIPELINE ----------------
python - << 'PY'
import json

mem_file = "$MEM"

data = json.load(open(mem_file))

history = data.get("history", [])

# -------- compress --------
if len(history) > 30:
    keep = history[-15:]
    old = history[:-15]
else:
    keep = history
    old = []

# archive
try:
    arch = json.load(open("$ARCH"))
except:
    arch = {"archive":[]}

arch["archive"] += old

json.dump(arch, open("$ARCH","w"), indent=2)
json.dump({"history": keep}, open("$MEM","w"), indent=2)

# -------- summary --------
summary_text = " ".join([str(x.get("entry","")) for x in old[-20:]])

summary = {
    "text": summary_text,
    "count": len(old)
}

json.dump(summary, open("$SUMMARY","w"), indent=2)

# -------- index --------
index = {}

for i, item in enumerate(keep):
    text = str(item.get("entry","")).lower()
    for word in text.split():
        word = word.strip()
        if not word:
            continue
        index.setdefault(word, []).append(i)

json.dump(index, open("$INDEX","w"), indent=2)

print("[OK] memory pipeline complete")
PY

echo "[IMA V2 FIX] done"
