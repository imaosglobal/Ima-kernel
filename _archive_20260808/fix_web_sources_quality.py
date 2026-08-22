from pathlib import Path

p=Path("learning/web_knowledge_collector.py")

text=p.read_text(encoding="utf8")


text=text.replace(
'''def best_answer(question):
    results=collect_sources(question)

    valid=[]

    for r in results:
        if validate_result(question,r):
            valid.append(r)

    if valid:
        return valid[0]

    return None
''',
'''def clean_source_result(r):

    if not r:
        return None

    content=r.get("content","").strip()

    if not content:
        return None

    if len(content)<20:
        return None

    return r


def best_answer(question):

    results=collect_sources(question)

    valid=[]

    for r in results:

        cleaned=clean_source_result(r)

        if cleaned and validate_result(question,cleaned):
            valid.append(cleaned)


    if valid:

        valid.sort(
            key=lambda x:x.get("confidence",0),
            reverse=True
        )

        return valid[0]


    return None
'''
)

p.write_text(text,encoding="utf8")

