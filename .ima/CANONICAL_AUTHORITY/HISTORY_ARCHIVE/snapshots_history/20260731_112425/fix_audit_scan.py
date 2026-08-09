from pathlib import Path

p = Path("ima_full_audit.py")
text = p.read_text(encoding="utf8")

old = 'py_files = list(ROOT.rglob("*.py"))'

new = '''EXCLUDED = [
    ".ima/backups",
    ".ima/archive",
    "archive",
    "snapshots",
    "__pycache__",
    "learning_backup",
    "broken_backup",
]

py_files = [
    x for x in ROOT.rglob("*.py")
    if not any(e in str(x) for e in EXCLUDED)
]'''

if old not in text:
    print("[FAIL] scan line not found")
else:
    text = text.replace(old, new)
    p.write_text(text, encoding="utf8")
    print("[OK] audit scan fixed")
