from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

addition = r'''

def guardian_target_compile(files):

    import py_compile


    errors=[]

    for f in files:
        if not f.endswith(".py"):
            continue

        try:
            py_compile.compile(f, doraise=True)

        except Exception as e:
            errors.append(f)

    return errors


'''

if "def guardian_target_compile" not in text:
    marker="def run_cycle():"
    text=text.replace(marker, addition+"\n"+marker)

p.write_text(text,encoding="utf8")

