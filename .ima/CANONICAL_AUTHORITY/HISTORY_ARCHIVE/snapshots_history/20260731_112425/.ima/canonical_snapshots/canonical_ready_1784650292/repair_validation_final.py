from pathlib import Path

p=Path("learning/web_knowledge_collector.py")
text=p.read_text(encoding="utf8")

start=text.find("def validate_result")
end=text.find("\ndef source_priority", start)

if start==-1 or end==-1:
    raise Exception("validation block not found")

new=r'''def validate_result(question,result):

    if not result:
        return False

    content=result.get("content","").strip()

    if len(content)<10:
        return False


    source=result.get("source","")


    # מקורות מוכרים עוברים אימות בסיסי
    if source in [
        "Wikipedia",
        "Wikidata"
    ]:
        return True


    # מקור פנימי
    q=normalize_term(question)
    if q in content.lower():
        return True


    return False


'''

text=text[:start]+new+text[end:]

p.write_text(text,encoding="utf8")

print("VALIDATION FINAL FIXED")
