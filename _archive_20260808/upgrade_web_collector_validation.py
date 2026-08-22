from pathlib import Path

p=Path("learning/web_knowledge_collector.py")

text=p.read_text(encoding="utf8")


text=text.replace(
'''def best_answer(question):

    results=collect_sources(question)

    if results:
        return results[0]

    return None
''',
'''
def validate_result(question,result):

    if not result:
        return False

    content=result.get("content","").strip()

    if len(content)<20:
        return False

    q=question.replace("מה זה ","").replace("מהי ","").lower()

    text=content.lower()

    words=q.split()

    hits=sum(
        1 for w in words
        if w in text
    )

    if hits==0:
        return False

    return True


def best_answer(question):

    results=collect_sources(question)

    valid=[]

    for r in results:
        if validate_result(question,r):
            valid.append(r)

    if valid:
        return valid[0]

    return None
'''
)


p.write_text(text,encoding="utf8")

