from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

if "import json" not in text.splitlines()[:10]:
    text = "import json\n" + text
    p.write_text(text, encoding="utf8")
else:
