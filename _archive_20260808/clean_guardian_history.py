from pathlib import Path

p = Path("ima_guardian_controller.py")
text = p.read_text(encoding="utf8")

start = text.index("# IMA_COMPACT_HISTORY")
end = text.index("from pathlib import Path", text.index("# IMA_HISTORY_LOGGER"))

new = '''# IMA_COMPACT_HISTORY
from pathlib import Path
import json
from datetime import datetime

def guardian_history(event, data=None):
    path = Path(".ima/guardian/history.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "time": datetime.now().isoformat(),
        "event": event,
        "data": data or {}
    }

    with path.open("a", encoding="utf8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\\n")


'''

text = text[:start] + new + text[end:]

p.write_text(text, encoding="utf8")

