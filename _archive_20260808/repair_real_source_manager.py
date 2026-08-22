from pathlib import Path

p=Path("learning/source_manager.py")

text=p.read_text(encoding="utf8")

text=text.replace(
'url="https://he.wikipedia.org/api/rest_v1/page/summary/"+question.replace(" ","_")',
'url="https://he.wikipedia.org/api/rest_v1/page/summary/"+question.strip().replace(" ","_")'
)

text=text.replace(
'if question in data:',
'''if question in data or ("מה זה "+question) in data:
            key = question if question in data else "מה זה "+question'''
)

text=text.replace(
'"content":data[question]["content"],',
'"content":data[key]["content"],'
)

p.write_text(text,encoding="utf8")

