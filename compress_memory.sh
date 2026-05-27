#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/ima_kernel"
MEM="$BASE/kernel/cloud/memory.json"
ARCH="$BASE/kernel/cloud/memory_archive.json"

mkdir -p "$BASE/kernel/cloud"

echo "[COMPRESS] loading memory..."

if [ ! -f "$MEM" ]; then
  echo "[COMPRESS] no memory file found"
  exit 0
fi

# אם אין ארכיון - ליצור
if [ ! -f "$ARCH" ]; then
  echo '{"archive":[]}' > "$ARCH"
fi

# חילוץ זיכרון
DATA=$(cat "$MEM")

# מספר רשומות
COUNT=$(echo "$DATA" | grep -o '"entry"' | wc -l)

echo "[COMPRESS] entries found: $COUNT"

# אם קטן מדי - לא עושים כלום
if [ "$COUNT" -lt 50 ]; then
  echo "[COMPRESS] memory too small, skipping"
  exit 0
fi

# מחלק: נשאיר 20 אחרונים
cat "$MEM" | python - << 'PY' > /tmp/ima_split.json
import json

data = json.load(open(0))

history = data.get("history", [])

keep = history[-20:]
old = history[:-20]

out = {
    "keep": keep,
    "old": old
}

print(json.dumps(out))
PY

KEEP=$(cat /tmp/ima_split.json | python -c "import sys,json; print(json.load(sys.stdin)['keep'])")
OLD=$(cat /tmp/ima_split.json | python -c "import sys,json; print(json.load(sys.stdin)['old'])")

# שמירת ארכיון
python - << 'PY'
import json

arch_file = "$ARCH"
data = json.load(open(arch_file))
old = json.load(open("/tmp/ima_split.json"))["old"]

data["archive"] += old

json.dump(data, open(arch_file, "w"), indent=2)
PY

# כתיבת זיכרון חדש (מנוקה)
python - << 'PY'
import json

keep = json.load(open("/tmp/ima_split.json"))["keep"]

new = {
    "history": keep,
    "lastSync": 0
}

json.dump(new, open("$MEM", "w"), indent=2)
PY

echo "[COMPRESS] done"
echo "[COMPRESS] kept: 20 latest entries"
echo "[COMPRESS] archived old memory"
