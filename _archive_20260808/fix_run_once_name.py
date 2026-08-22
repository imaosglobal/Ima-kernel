from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

text = text.replace(
    "        run_once()",
    "        run_cycle()"
)

p.write_text(text, encoding="utf8")

