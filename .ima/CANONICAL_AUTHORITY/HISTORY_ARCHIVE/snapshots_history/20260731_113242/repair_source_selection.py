from pathlib import Path

p=Path("learning/web_knowledge_collector.py")

text=p.read_text(encoding="utf8")


old='''def source_priority(result):

    if not result:
        return 0

    source=result.get("source","")

    if source=="Wikipedia":
        return 100

    if source=="Wikidata":
        return 50

    return 10
'''


new='''def source_priority(result):

    if not result:
        return 0

    source=result.get("source","")
    content=result.get("content","")

    score=0

    if source=="Wikipedia":
        score += 100

    if source=="Wikidata":
        score += 20

    if len(content)>200:
        score += 50

    if len(content)<50:
        score -= 50

    return score
'''


text=text.replace(old,new)


# הסרת Wikidata כתשובה ראשית אם יש Wikipedia
text=text.replace(
'''    if valid:
        return valid[0]
''',
'''    if valid:

        wikipedia=[
            x for x in valid
            if x.get("source")=="Wikipedia"
        ]

        if wikipedia:
            return wikipedia[0]

        return valid[0]
'''
)


p.write_text(text,encoding="utf8")

print("SOURCE SELECTION REPAIRED")
