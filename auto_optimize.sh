#!/bin/bash
set -e
cd ~/ima_kernel
DATE=$(date +%Y%m%d_%H%M%S)
ARCHIVE="_archive_20260808"
mkdir -p "$ARCHIVE"

echo "=== Checkpoint before changes ==="
git add -A && git commit -m "checkpoint before auto_optimize $DATE" -q --allow-empty || true

echo "=== Finding unused files ==="
> _unimported_candidates.txt
for f in *.py; do
  if [ "$f" = "app.py" ]; then continue; fi
  name="${f%.py}"
  count=$(grep -rl "import $name" . --include="*.py" 2>/dev/null | grep -v "_archive" | grep -v "^./$f$" | wc -l)
  shcount=$(grep -rl "$name.py" . --include="*.sh" 2>/dev/null | grep -v "_archive" | wc -l)
  if [ "$count" -eq 0 ] && [ "$shcount" -eq 0 ]; then echo "$f"; fi
done > _unimported_candidates.txt

MOVED=0
while read -r f; do
  if [ -z "$f" ]; then continue; fi
  mv "$f" "$ARCHIVE/" && MOVED=$((MOVED+1))
done < _unimported_candidates.txt

echo "=== Dead code check on remaining files ==="
vulture *.py --min-confidence 80 > "$ARCHIVE/vulture_report_$DATE.txt" 2>&1 || true

echo "=== Restarting server ==="
pkill -f "python3 app.py" 2>/dev/null || true
sleep 1
nohup python3 app.py > "$ARCHIVE/server_log_$DATE.txt" 2>&1 &
sleep 2

echo "=== Health check ==="
if curl -sf http://127.0.0.1:5001/health > /dev/null; then
  echo "OK -- committing archive of $MOVED files"
  echo "## $DATE" >> "$ARCHIVE/ARCHIVE_LOG.md"
  echo "$MOVED files archived automatically. See vulture_report_$DATE.txt" >> "$ARCHIVE/ARCHIVE_LOG.md"
  git add -A && git commit -m "auto_optimize: archived $MOVED unused files ($DATE)" -q
  echo "=== Done. $MOVED files archived, server healthy, committed. ==="
else
  echo "HEALTH CHECK FAILED -- rolling back"
  git reset --hard HEAD -q
  pkill -f "python3 app.py" 2>/dev/null || true
  nohup python3 app.py > /dev/null 2>&1 &
  echo "=== Rolled back. Nothing archived. Check server_log_$DATE.txt ==="
fi
