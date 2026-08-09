from pathlib import Path

p=Path("learning/web_knowledge_collector.py")
text=p.read_text(encoding="utf8")

start=text.find("def validate_result")
end=text.find("\ndef source_priority", start)

if start==-1:
    raise Exception("validate_result not found")

new=r'''
def validate_result(question,result):

    if not result:
        return False

    content=result.get("content","").strip()
    source=result.get("source","")


    # מקורות חיצוניים מאומתים
    if source in [
        "Wikipedia",
        "Wikidata"
    ]:
        return True


    # מקור פנימי
    if len(content)>=10:
        return True


    return False


'''

text=text[:start]+new+text[end:]

p.write_text(text,encoding="utf8")

print("UNIFIED VALIDATION FIXED")
