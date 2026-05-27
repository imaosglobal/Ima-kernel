#!/data/data/com.termux/files/usr/bin/bash
set -e

BASE="$HOME/ima_kernel/kernel/cloud"

MEM="$BASE/memory.json"
ARCH="$BASE/memory_archive.json"
INDEX="$BASE/memory_index.json"
SUMMARY="$BASE/memory_summary.json"

echo "[IMA REBUILD] starting..."

mkdir -p "$BASE"

# ensure base files exist
[ -f "$MEM" ] || echo '{"memory":[]}' > "$MEM"
[ -f "$ARCH" ] || echo '{"archive":[]}' > "$ARCH"

python3 - << 'PY'
import json, os

BASE = os.path.expanduser("~/ima_kernel/kernel/cloud")

MEM = os.path.join(BASE, "memory.json")
ARCH = os.path.join(BASE, "memory_archive.json")
INDEX = os.path.join(BASE, "memory_index.json")
SUMMARY = os.path.join(BASE, "memory_summary.json")

def safe_load(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except:
        return {}

def normalize(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if "memory" in data:
            return data["memory"]
        if "archive" in data:
            return data["archive"]
    return []

mem = normalize(safe_load(MEM))
arch = normalize(safe_load(ARCH))

items = mem + arch

# -------- index --------
index = {}
for i, item in enumerate(items):
    text = str(item.get("entry","")).lower()
    for word in text.split():
        word = word.strip()
        if not word:
            continue
        index.setdefault(word, []).append(i)

# -------- summary --------
summary = {
    "total_entries": len(items),
    "last_entry": items[-1] if items else None,
    "types": {}
}

for item in items:
    t = item.get("type","unknown")
    summary["types"][t] = summary["types"].get(t,0) + 1

with open(INDEX, "w", encoding="utf-8") as f:
    json.dump(index, f, indent=2, ensure_ascii=False)

with open(SUMMARY, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print("[OK] memory index + summary rebuilt safely")
PY

echo "[DONE] stable memory pipeline"
