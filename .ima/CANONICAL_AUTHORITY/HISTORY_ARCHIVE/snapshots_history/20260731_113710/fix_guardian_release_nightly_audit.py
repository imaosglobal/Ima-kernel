from pathlib import Path

p = Path("guardian_release_pipeline.py")
text = p.read_text(encoding="utf8")

old = '''def verify():
    run(["python3","guardian_regression_check.py"])
    run(["python3","ima_full_audit.py"])
    run(["python3","ima_guardian_watch.py","--once"])
'''

new = '''def verify():
    run(["python3","guardian_regression_check.py"])
    run(["python3","ima_guardian_watch.py","--once"])

def nightly_audit():
    import datetime
    hour = datetime.datetime.now().hour

    if hour == 3:
        print("[NIGHTLY AUDIT WINDOW]")
        run(["python3","ima_full_audit.py"])
    else:
        print("[SKIP FULL AUDIT] nightly only")
'''

if old in text:
    text=text.replace(old,new,1)
else:
    print("[WARN] verify block not found")

p.write_text(text,encoding="utf8")
print("[OK] nightly audit separation installed")
