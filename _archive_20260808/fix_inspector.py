from pathlib import Path

p=Path("learning/sources/source_inspector.py")

text=p.read_text(encoding="utf8")

text=text.replace(
'''if r.status == 200:
                score += 40''',
'''if r.status == 200:
                score += 40
            elif r.status in [301,302,403]:
                score += 20'''
)

p.write_text(text,encoding="utf8")

