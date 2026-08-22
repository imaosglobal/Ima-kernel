from pathlib import Path
import subprocess
import json
from datetime import datetime

history = Path(".ima/guardian/history.jsonl")
history.parent.mkdir(parents=True, exist_ok=True)

existing = set()

if history.exists():
    for line in history.read_text(encoding="utf8").splitlines():
        try:
            existing.add(json.loads(line).get("commit"))
        except:
            pass

r = subprocess.run(
    ["git", "log", "--format=%H|%ad|%s", "--date=iso"],
    capture_output=True,
    text=True
)

added = 0

with history.open("a", encoding="utf8") as f:
    for line in r.stdout.splitlines():
        sha, date, msg = line.split("|", 2)

        if sha in existing:
            continue

        record = {
            "time": date,
            "event": "git_history_import",
            "commit": sha,
            "message": msg
        }

        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        added += 1

