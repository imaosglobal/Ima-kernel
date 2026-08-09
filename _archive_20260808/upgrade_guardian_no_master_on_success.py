from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

old = '''            if errors:
                print("[TARGET REPAIR]", errors)
                import subprocess
                subprocess.run(
                    ["python3","ima_guardian_self_repair.py"]
                )

            print("[OK] incremental cycle executed")
'''

new = '''            if errors:
                print("[TARGET REPAIR]", errors)
                import subprocess
                subprocess.run(
                    ["python3","ima_guardian_self_repair.py"]
                )
                return

            print("[OK] target files healthy")
            return
'''

if old in text:
    text=text.replace(old,new,1)
else:
    print("[WARN] block not found")

p.write_text(text,encoding="utf8")

print("[OK] master bypass on healthy targets added")
