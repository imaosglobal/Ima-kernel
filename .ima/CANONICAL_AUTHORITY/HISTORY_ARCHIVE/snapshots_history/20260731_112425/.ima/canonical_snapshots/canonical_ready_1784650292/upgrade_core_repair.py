from pathlib import Path

p=Path("ima_guardian_core.py")

text=p.read_text(encoding="utf8")

old='''"python3 ima_full_audit.py",'''

new='''"python3 ima_full_audit.py",
        "python3 ima_guardian_self_repair.py",'''

text=text.replace(old,new)

p.write_text(text,encoding="utf8")

print("[OK] repair connected")
