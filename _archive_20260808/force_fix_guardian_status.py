from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

# הסרת קריאות/הגדרות פגומות קיימות
lines = text.splitlines()

out = []
skip = False

for line in lines:
    if line.startswith("def guardian_status"):
        skip = True
        continue

    if skip:
        if line.startswith("def ") and "guardian_status" not in line:
            skip = False
            out.append(line)
        elif line.startswith("if __name__"):
            skip = False
            out.append(line)
        else:
            continue
    else:
        out.append(line)

text = "\n".join(out)

insert = '''

def guardian_status():
    from pathlib import Path


    data = {
        "controller": Path("ima_guardian_controller.py").exists(),
        "master": Path("ima_guardian_master.py").exists(),
        "policy": Path(".ima/guardian/policy.json").exists(),
        "history": Path(".ima/guardian/history.jsonl").exists(),
        "smart_state": Path(".ima/guardian/smart_state.json").exists()
    }

    for key, value in data.items():

'''

pos = text.find("def run_cycle")

if pos != -1:
    text = text[:pos] + insert + text[pos:]
else:
    text += insert

p.write_text(text, encoding="utf8")

