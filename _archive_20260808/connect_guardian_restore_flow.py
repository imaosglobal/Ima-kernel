from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

if "guardian_restore_core()" not in text:

    insert = '''
def guardian_restore_check():
    try:
        from upgrade_guardian_snapshot_restore import guardian_restore_core
        guardian_restore_core()
    except Exception as e:

'''

    text = insert + text

    old = '''def run_cycle():

    new = '''def run_cycle():
    guardian_restore_check()'''

    if old in text:
        text = text.replace(old, new, 1)

p.write_text(text, encoding="utf8")
