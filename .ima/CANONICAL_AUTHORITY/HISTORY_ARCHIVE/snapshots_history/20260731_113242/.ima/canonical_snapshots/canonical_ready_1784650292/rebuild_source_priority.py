from pathlib import Path

p=Path("learning/web_knowledge_collector.py")

text=p.read_text(encoding="utf8")


insert=r'''

def source_priority(result):

    if not result:
        return 0

    source=result.get("source","")

    if source=="Wikipedia":
        return 100

    if source=="Wikidata":
        return 50

    return 10


'''

if "def source_priority" not in text:
    pos=text.find("def best_answer")
    text=text[:pos]+insert+text[pos:]


old="""        valid.sort(
            key=lambda x:x.get("confidence",0),
            reverse=True
        )
"""

new="""        valid.sort(
            key=lambda x:(
                source_priority(x),
                x.get("confidence",0)
            ),
            reverse=True
        )
"""

text=text.replace(old,new)


p.write_text(text,encoding="utf8")

print("SOURCE PRIORITY REBUILT")
