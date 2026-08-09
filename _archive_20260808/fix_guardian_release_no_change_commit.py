from pathlib import Path

p = Path("guardian_release_pipeline.py")
text = p.read_text(encoding="utf8")

old = '''def commit():
    run(["git","add","-A"])
    msg=f"IMA automatic guarded commit {datetime.now().isoformat()}"
    run(["git","commit","-m",msg])
'''

new = '''def commit():
    run(["git","add","-A"])

    status = subprocess.run(
        ["git","diff","--cached","--quiet"]
    )

    if status.returncode == 0:
        print("[NO CHANGES] commit skipped")
        return False

    msg=f"IMA automatic guarded commit {datetime.now().isoformat()}"
    run(["git","commit","-m",msg])
    return True
'''

if old in text:
    text=text.replace(old,new,1)
else:
    print("[WARN] commit block not found")

p.write_text(text,encoding="utf8")
print("[OK] no-change commit handling installed")
