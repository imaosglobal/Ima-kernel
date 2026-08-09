from pathlib import Path

p = Path("ima_full_audit.py")

text = p.read_text(encoding="utf8")

insert = r'''
EXCLUDED_DIRS = {
    ".ima/backups",
    ".ima/archive",
    "archive",
    "snapshots",
    "__pycache__",
}

def should_skip(path):
    s = str(path)
    return any(x in s for x in EXCLUDED_DIRS) or "broken_backup" in s or "learning_backup" in s
'''

if "EXCLUDED_DIRS" not in text:
    text = insert + "\n" + text

text = text.replace(
    "for p in ROOT.rglob(\"*.py\"):",
    "for p in ROOT.rglob(\"*.py\"):\n    if should_skip(p):\n        continue"
)

p.write_text(text, encoding="utf8")

print("[OK] audit optimizer installed")
