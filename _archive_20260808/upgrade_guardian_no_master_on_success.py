from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

old = '''            if errors:
                import subprocess
                subprocess.run(
                    ["python3","ima_guardian_self_repair.py"]
                )

'''

new = '''            if errors:
                import subprocess
                subprocess.run(
                    ["python3","ima_guardian_self_repair.py"]
                )
                return

            return
'''

if old in text:
    text=text.replace(old,new,1)
else:

p.write_text(text,encoding="utf8")

