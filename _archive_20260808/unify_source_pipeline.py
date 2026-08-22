from pathlib import Path

p=Path("learning/web_knowledge_collector.py")
text=p.read_text(encoding="utf8")

start=text.find("def collect_sources_priority")
end=text.find("\ndef best_answer", start)

if start==-1 or end==-1:
    raise Exception("source blocks not found")

new=r'''
def collect_sources_unified(question):

    results=[]

    # ניקוי שאלה
    term=normalize_term(question)


    # Wikipedia
    try:
        r=wikipedia(term)

        if r:
            r["priority"]=100
            results.append(r)

    except Exception:
        pass


    # Wikidata
    try:
        r=wikidata(term)

        if r:
            r["priority"]=50
            results.append(r)

    except Exception:
        pass


    # מקורות פנימיים של IMA
    try:
        r=get_real_source(question)

        if r:
            r["priority"]=80
            results.append(r)

    except Exception:
        pass


    return results


'''


text=text[:start]+new+text[end:]

# החלפת שימוש בישן
text=text.replace(
"results=collect_sources_priority(question)",
"results=collect_sources_unified(question)"
)

# אם best_answer עדיין משתמש collect_sources ישן
text=text.replace(
"results=collect_sources(question)",
"results=collect_sources_unified(question)"
)


p.write_text(text,encoding="utf8")

