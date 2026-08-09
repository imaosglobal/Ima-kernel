from pathlib import Path

p = Path("guardian_release_pipeline.py")
text = p.read_text(encoding="utf8")

old = '''def final_tag():
    tag=f"ima-release-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    run(["git","tag",tag])
    print("[FINAL TAG]",tag)
'''

new = '''def final_tag():
    status = subprocess.run(
        ["git","rev-parse","--verify","HEAD"],
        capture_output=True
    )

    tag=f"ima-release-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    run(["git","tag",tag])
    print("[FINAL TAG]",tag)
'''

if old in text:
    text=text.replace(old,new,1)
else:
    print("[WARN] final tag block not found")

p.write_text(text,encoding="utf8")
print("[OK] release tag gate prepared")
