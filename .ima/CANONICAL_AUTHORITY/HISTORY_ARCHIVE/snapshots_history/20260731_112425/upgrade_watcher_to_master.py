from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

old = "ima_guardian_controller.py"
new = "ima_guardian_master.py"

count = text.count(old)

if count:
    text = text.replace(old, new)
    p.write_text(text, encoding="utf8")
    print("[OK] watcher redirected to master:", count)
else:
    print("[WARN] controller reference not found")
