#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/ima_kernel"
MEM="$BASE/kernel/cloud/memory.json"
ARCH="$BASE/kernel/cloud/memory_archive.json"
INDEX="$BASE/kernel/cloud/memory_index.json"
SUMMARY="$BASE/kernel/cloud/memory_summary.json"

mkdir -p "$BASE/kernel/cloud"

# ---------- LOAD ----------
if [ ! -f "$MEM" ]; then
  echo '{"history":[]}' > "$MEM"
fi

# ---------- COMPRESS ----------
echo "[IMA MEMORY] compressing..."

python - << 'PY'
import json

mem_file = open("$MEM").read()
data = json.loads(mem_file)

history = data.get("history", [])

if len(history) < 30:
    print("[SKIP] not enough data")
    exit()

keep = history[-15:]
old = history[:-15]

# archive
try:
    arch = json.load(open("$ARCH"))
except:
    arch = {"archive":[]}

arch["archive"] += old

json.dump(arch, open("$ARCH","w"), indent=2)

json.dump({"history": keep}, open("$MEM","w"), indent=2)
print("[OK] compressed")
PY

# ---------- SUMMARIZE OLD ----------
echo "[IMA MEMORY] summarizing old memory..."

python - << 'PY'
import json

try:
    arch = json.load(open("$ARCH"))
except:
    arch = {"archive":[]}

old = arch.get("archive", [])[-50:]

if not old:
    exit()

summary = {
    "summary": " | ".join([str(x.get("entry","")) for x in old][-10:]),
    "count": len(old),
    "updated": True
}

json.dump(summary, open("$SUMMARY","w"), indent=2)
print("[OK] summarized")
PY

# ---------- INDEX ----------
echo "[IMA MEMORY] indexing..."

python - << 'PY'
import json

try:
    mem = json.load(open("$MEM"))
except:
    mem = {"history":[]}

index = {}

for i, item in enumerate(mem.get("history", [])):
    text = item.get("entry","")
    for word in str(text).split():
        word = word.lower()
        index.setdefault(word, []).append(i)

json.dump(index, open("$INDEX","w"), indent=2)
print("[OK] indexed")
PY

echo "[IMA MEMORY ENGINE V2 READY]"
