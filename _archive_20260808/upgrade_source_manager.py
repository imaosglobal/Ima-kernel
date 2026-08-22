from pathlib import Path

p=Path("learning/source_manager.py")

text=p.read_text(encoding="utf8")

text=text.replace(
'url="https://he.wikipedia.org/api/rest_v1/page/summary/"+question.strip().replace(" ","_")',
'''
term=question.replace("מה זה ","").strip()

url="https://he.wikipedia.org/api/rest_v1/page/summary/"+term.replace(" ","_")
'''
)

p.write_text(text,encoding="utf8")

