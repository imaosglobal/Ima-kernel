
from pathlib import Path

MAX = 2000

p = Path('.ima/guardian/history.jsonl')

if p.exists():
    lines = p.read_text(encoding='utf8').splitlines()

    if len(lines) > MAX:
        p.write_text(
            "\n".join(lines[-MAX:]) + "\n",
            encoding="utf8"
        )
        print("[OK] history compacted")
    else:
        print("[OK] history size healthy")
