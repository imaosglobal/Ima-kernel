from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

old = '''            incremental_cycle()

            if changed is False:
                return

'''

new = '''            changed_files = smart_diff()

            if not changed_files:
                return

            errors = guardian_target_compile(changed_files)

            if errors:
                import subprocess
                subprocess.run(
                    ["python3","ima_guardian_self_repair.py"]
                )

'''

if old not in text:
else:
    text=text.replace(old,new,1)

p.write_text(text,encoding="utf8")

