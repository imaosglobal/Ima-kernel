from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

if "guardian_restore_core()" not in text:

    insert = '''
def guardian_restore_check():
    try:
        from upgrade_guardian_snapshot_restore import guardian_restore_core
        guardian_restore_core()
        print("[OK] snapshot restore check")
    except Exception as e:
        print("[RESTORE CHECK ERROR]", e)

'''

    text = insert + text

    old = '''def run_cycle():
    print("\\n=== GUARDIAN AUTO CYCLE ===")'''

    new = '''def run_cycle():
    print("\\n=== GUARDIAN AUTO CYCLE ===")
    guardian_restore_check()'''

    if old in text:
        text = text.replace(old, new, 1)

p.write_text(text, encoding="utf8")
print("[OK] guardian restore flow connected")
