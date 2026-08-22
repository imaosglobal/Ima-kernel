from pathlib import Path
import json
import subprocess
from datetime import datetime

base = Path(".ima/guardian")
base.mkdir(parents=True, exist_ok=True)

history = base / "history.jsonl"
state = base / "state.json"

if not history.exists():
    history.write_text("", encoding="utf8")

if not state.exists():
    state.write_text(
        json.dumps({
            "installed": str(datetime.now()),
            "cycles": 0
        }, indent=2),
        encoding="utf8"
    )

p = Path("ima_guardian_controller.py")

if not p.exists():
    raise SystemExit(1)

text = p.read_text(encoding="utf8")

marker = "# IMA_HISTORY_LOGGER"

if marker not in text:

    insert = r'''

# IMA_HISTORY_LOGGER

def guardian_history(event, data=None):

    from pathlib import Path
    import json
    from datetime import datetime

    path = Path(".ima/guardian/history.jsonl")

    record = {
        "time": str(datetime.now()),
        "event": event,
        "data": data or {}
    }

    with path.open("a", encoding="utf8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

'''

    text = insert + "\n" + text

    text = text.replace(
    )

    text = text.replace(
    )

    p.write_text(text, encoding="utf8")

