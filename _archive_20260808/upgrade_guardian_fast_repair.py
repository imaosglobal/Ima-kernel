from pathlib import Path

# תיקון audit exclusions
p = Path("ima_full_audit.py")
if p.exists():
    text = p.read_text(encoding="utf8")

    if "broken_runtime_backup" not in text:
        text = text.replace(
            'EXCLUDED = [',
            '''EXCLUDED = [
    ".ima/broken_runtime_backup.py",
    ".ima/backups",
    ".ima/archive",
    "archive",
    "snapshots",'''
        )

    p.write_text(text, encoding="utf8")


# תיקון controller - תיקון רק כשיש שגיאות
p = Path("ima_guardian_controller.py")
text = p.read_text(encoding="utf8")

old = 'run("python3 ima_guardian_autofix.py")'

new = '''
if errors:
    run("python3 ima_guardian_autofix.py")
else:
    log("[SKIP] autofix no errors")
'''

text = text.replace(old,new)

p.write_text(text,encoding="utf8")


