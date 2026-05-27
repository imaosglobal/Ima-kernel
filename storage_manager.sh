#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"
LOGDIR="$ROOT/runtime/logs"
MEMDIR="$ROOT/kernel"

echo "[STORAGE] scanning kernel..."

# 1. ניקוי לוגים מעל 5MB
find "$LOGDIR" -type f -name "*.log" -size +5M -exec rm -f {} \;

# 2. כיווץ memory אם גדול מדי
MEMFILE="$MEMDIR/core/memory.js"

if [ -f "$MEMFILE" ]; then
  SIZE=$(stat -c%s "$MEMFILE" 2>/dev/null || echo 0)

  if [ "$SIZE" -gt 500000 ]; then
    echo "[STORAGE] trimming memory file"

    # שומר רק 50% אחרונים (פשטני אבל עובד)
    head -n 200 "$MEMFILE" > "$MEMFILE.tmp" && mv "$MEMFILE.tmp" "$MEMFILE"
  fi
fi

# 3. ניקוי watchdog logs ישנים
find "$ROOT" -name "watchdog*.log" -size +2M -delete

echo "[STORAGE] done"
