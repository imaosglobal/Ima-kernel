from pathlib import Path

p=Path("learning/web_knowledge_collector.py")
text=p.read_text(encoding="utf8")

start=text.find("def collect_sources(question):")
end=text.find("\ndef normalize_term", start)

if start==-1 or end==-1:
    raise Exception("collect_sources block not found")


new=r'''def collect_sources(question):

    results=[]

    term=normalize_term(question)


    # Wikipedia ראשון
    try:
        r=wikipedia(term)
        if r:
            r["priority"]=100
            results.append(r)
    except Exception:
        pass


    # Wikidata שני
    try:
        r=wikidata(term)
        if r:
            r["priority"]=50
            results.append(r)
    except Exception:
        pass


    return sorted(
        results,
        key=lambda x:(
            x.get("priority",0),
            x.get("confidence",0),
            len(x.get("content",""))
        ),
        reverse=True
    )


'''

text=text[:start]+new+text[end:]

p.write_text(text,encoding="utf8")

print("COLLECT SOURCES PRIORITY FIXED")
