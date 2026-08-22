from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

if "guardian_policy_check" not in text:

    addition = r'''

def guardian_policy_check():
    import json

    p = Path(".ima/guardian/policy.json")

    if not p.exists():
        return False

    try:
        data=json.loads(p.read_text(encoding="utf8"))
        return data.get("rules",{}).get(
            "scan_only_changed_files",
            False
        )
    except Exception:
        return False
'''

    text = addition + "\n" + text


old = '''def run_cycle():
'''

new = '''def run_cycle():

    if not guardian_policy_check():
        return
'''

if old in text:
    text=text.replace(old,new,1)

p.write_text(text,encoding="utf8")

