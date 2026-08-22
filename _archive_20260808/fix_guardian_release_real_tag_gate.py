from pathlib import Path

p = Path("guardian_release_pipeline.py")
text = p.read_text(encoding="utf8")

old = '''def main():
    tag_base()
    verify()
    commit()
    final_tag()
'''

new = '''def main():

    tag_base()

    verify()

    changed = commit()

    if not changed:
        return

    final_tag()

'''

if old in text:
    text=text.replace(old,new,1)
else:

p.write_text(text,encoding="utf8")
