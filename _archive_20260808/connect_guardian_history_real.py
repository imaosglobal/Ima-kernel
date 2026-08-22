from pathlib import Path

p = Path("ima_guardian_controller.py")
text = p.read_text(encoding="utf8")

marker = "# IMA_COMPACT_HISTORY"

if marker not in text:

    block = r'''
# IMA_COMPACT_HISTORY

def guardian_history(event, data=None):
    from pathlib import Path
    import json
    from datetime import datetime

    path = Path(".ima/guardian/history.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "time": datetime.now().isoformat(),
        "event": event,
        "data": data or {}
    }

    with path.open("a", encoding="utf8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

'''

    text = block + "\n" + text

text = text.replace(
    'log("=== IMA GUARDIAN CONTROLLER START ===")',
    'guardian_history("cycle_start")\n    log("=== IMA GUARDIAN CONTROLLER START ===")'
)

text = text.replace(
    'log(\n        "=== IMA GUARDIAN CONTROLLER END ==="',
    'guardian_history("cycle_end")\n    log(\n        "=== IMA GUARDIAN CONTROLLER END ==="'
)

p.write_text(text, encoding="utf8")

