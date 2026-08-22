from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

if "guardian_protect_core" not in text:

    addition = r'''

def guardian_protect_core():
    import py_compile

    files=[
        "ima_guardian_watch.py",
        "ima_guardian_self_repair.py",
        "ima_guardian_master.py",
        "ima_guardian_controller.py"
    ]

    for f in files:
        try:
            py_compile.compile(f,doraise=True)
        except Exception as e:
            return False

    return True
'''

    text = addition + "\n" + text


old='''def run_cycle():
'''

new='''def run_cycle():

    if not guardian_protect_core():
        return
'''

if old in text:
    text=text.replace(old,new,1)

p.write_text(text,encoding="utf8")

