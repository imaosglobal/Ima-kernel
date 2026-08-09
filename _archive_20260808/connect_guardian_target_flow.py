from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

old = '''            incremental_cycle()

            if changed is False:
                print("[SMART STOP] no changes detected")
                return

            print("[OK] incremental cycle executed")
'''

new = '''            changed_files = smart_diff()

            if not changed_files:
                print("[SMART STOP] no changes detected")
                return

            errors = guardian_target_compile(changed_files)

            if errors:
                print("[TARGET REPAIR]", errors)
                import subprocess
                subprocess.run(
                    ["python3","ima_guardian_self_repair.py"]
                )

            print("[OK] incremental cycle executed")
'''

if old not in text:
    print("[WARN] target block not found")
else:
    text=text.replace(old,new,1)

p.write_text(text,encoding="utf8")

print("[OK] target repair flow connected")
