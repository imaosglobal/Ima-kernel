from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

old = '''    if not changed:
        return
'''

new = '''    if not changed:
        return False
'''

if old in text:
    text=text.replace(old,new,1)

old2 = '''    python_changed = [
        x for x in changed
        if x.endswith(".py")
    ]
'''

new2 = '''    python_changed = [
        x for x in changed
        if x.endswith(".py")
    ]

    if not python_changed:
        return False
'''

if old2 in text:
    text=text.replace(old2,new2,1)

# הוספת return בסוף הפונקציה לפני הפונקציה הבאה
marker = "def run_cycle():"
pos = text.find(marker)

before = text[:pos]
after = text[pos:]

if "return True" not in before[-500:]:
    before = before.rstrip() + "\n\n    return True\n\n"

text = before + after

p.write_text(text,encoding="utf8")
