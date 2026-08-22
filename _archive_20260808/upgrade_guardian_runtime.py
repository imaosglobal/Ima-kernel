import subprocess
from pathlib import Path

p = Path("ima_guardian_controller.py")
text = p.read_text(encoding="utf8")

text = text.replace(
'''    r = subprocess.run(
        cmd,
        shell=True,
        text=True,
        capture_output=True
    )''',
'''    r = subprocess.run(
        cmd,
        shell=True,
        text=True,
        capture_output=True,
        timeout=300
    )'''
)

if "timeout=300" in text:
else:

p.write_text(text, encoding="utf8")


# history compactor
h = Path(".ima/guardian/history_compactor.py")

h.write_text("""
from pathlib import Path

MAX = 2000

p = Path('.ima/guardian/history.jsonl')

if p.exists():
    lines = p.read_text(encoding='utf8').splitlines()

    if len(lines) > MAX:
        p.write_text(
            "\\n".join(lines[-MAX:]) + "\\n",
            encoding="utf8"
        )
    else:
""", encoding="utf8")

