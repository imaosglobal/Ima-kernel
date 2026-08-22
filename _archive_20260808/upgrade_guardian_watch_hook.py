from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

old = '''def run_cycle():
    subprocess.run(
        ["python3", "ima_guardian_master.py"]
    )
'''

new = '''def run_cycle():
    try:
        if "guardian_incremental_check" in globals():
            guardian_incremental_check()
    except Exception as e:

    subprocess.run(
        ["python3", "ima_guardian_master.py"]
    )
'''

if old in text:
    text = text.replace(old,new,1)
else:

p.write_text(text,encoding="utf8")

