from pathlib import Path
import shutil
import time

p = Path("learning/sources/source_learning_daemon.py")

backup = p.with_suffix(".backup_fix_pipeline.py")
shutil.copy2(p, backup)

text = p.read_text(encoding="utf8")

# הסרת חיבור כפול מתוך scan_sources
lines = text.splitlines()

new=[]
inside_scan=False
removed=False

for line in lines:
    if line.startswith("def scan_sources"):
        inside_scan=True

    if inside_scan and "discover_cycle()" in line:
        if not removed:
            removed=True
            continue

    if inside_scan and line.startswith("def learning_cycle"):
        inside_scan=False

    new.append(line)

text="\n".join(new)+"\n"

p.write_text(text,encoding="utf8")

