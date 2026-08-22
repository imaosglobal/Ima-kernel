from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

old = '''            incremental_cycle()
'''

new = '''            changed = incremental_cycle()

            if changed is False:
                return

'''

if old in text:
    text=text.replace(old,new,1)
else:

p.write_text(text,encoding="utf8")
