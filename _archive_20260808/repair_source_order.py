from pathlib import Path

p=Path("learning/web_knowledge_collector.py")
text=p.read_text(encoding="utf8")

text=text.replace(
'''results=collect_sources(question)''',
'''results=collect_sources_priority(question)'''
)

insert=r'''

def normalize_term(q):

    return (
        q.replace("מה זה ","")
         .replace("מהי ","")
         .replace("?","")
         .strip()
    )


def collect_sources_priority(question):

    results=[]

    term=normalize_term(question)


    # Wikipedia קודם
    try:
        wiki=wikipedia_search(term)

        if wiki:
            results.append(wiki)

    except Exception:
        pass


    # Wikidata רק אחרי
    try:
        data=wikidata_search(term)

        if data:
            results.append(data)

    except Exception:
        pass


    return results

'''

pos=text.find("def best_answer")

text=text[:pos]+insert+"\n"+text[pos:]

p.write_text(text,encoding="utf8")

