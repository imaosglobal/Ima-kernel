from pathlib import Path

p = Path("ima_guardian_controller.py")
text = p.read_text(encoding="utf8")

start = text.index("# IMA_COMPACT_HISTORY")
end = text.index("from pathlib import Path", start)

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
        f.write(json.dumps(record, ensure_ascii=False) + "\\\\n")

'''

text = text[:start] + new + text[end:]

text = text.replace(
'guardian_history("cycle_start")',
'guardian_history("cycle_start", {"phase":"begin"})'
)

text = text.replace(
'guardian_history("cycle_end")',
'''guardian_history(
        "cycle_end",
        {
            "syntax_errors": errors,
            "phase":"complete"
        }
    )'''
)

p.write_text(text, encoding="utf8")

