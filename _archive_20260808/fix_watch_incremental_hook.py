from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

old = '''def run_cycle():

'''

new = '''def run_cycle():


    try:
        if "incremental_cycle" in globals():
            incremental_cycle()
    except Exception as e:
'''

if old not in text:
else:
    text = text.replace(old, new, 1)
    p.write_text(text, encoding="utf8")
