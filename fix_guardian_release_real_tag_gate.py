from pathlib import Path

p = Path("guardian_release_pipeline.py")
text = p.read_text(encoding="utf8")

old = '''def main():
    print("=== IMA GUARDED RELEASE PIPELINE ===")
    tag_base()
    verify()
    commit()
    final_tag()
    print("[DONE]")
'''

new = '''def main():
    print("=== IMA GUARDED RELEASE PIPELINE ===")

    tag_base()

    verify()

    changed = commit()

    if not changed:
        print("[STOP] no release created")
        return

    final_tag()

    print("[DONE]")
'''

if old in text:
    text=text.replace(old,new,1)
else:
    print("[WARN] main pipeline block not found")

p.write_text(text,encoding="utf8")
print("[OK] real release gate connected")
