from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

old = '''            incremental_cycle()
            print("[OK] incremental cycle executed")
'''

new = '''            changed = incremental_cycle()

            if changed is False:
                print("[SMART STOP] no changes detected")
                return

            print("[OK] incremental cycle executed")
'''

if old in text:
    text=text.replace(old,new,1)
else:
    print("[WARN] target not found")

p.write_text(text,encoding="utf8")
print("[OK] smart gate added")
