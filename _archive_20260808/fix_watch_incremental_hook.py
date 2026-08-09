from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

old = '''def run_cycle():

    print("\\n=== GUARDIAN AUTO CYCLE ===")
'''

new = '''def run_cycle():

    print("\\n=== GUARDIAN AUTO CYCLE ===")

    try:
        if "incremental_cycle" in globals():
            incremental_cycle()
            print("[OK] incremental cycle executed")
    except Exception as e:
        print("[INCREMENTAL ERROR]", e)
'''

if old not in text:
    print("[FAIL] run_cycle target not found")
else:
    text = text.replace(old, new, 1)
    p.write_text(text, encoding="utf8")
    print("[OK] incremental hook connected")
