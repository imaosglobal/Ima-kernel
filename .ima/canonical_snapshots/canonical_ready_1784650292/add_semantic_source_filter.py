from pathlib import Path

p=Path("learning/web_knowledge_collector.py")
text=p.read_text(encoding="utf8")

start=text.find("def validate_result")
end=text.find("\ndef source_priority", start)

new=r'''
def semantic_match(question,result):

    q=normalize_term(question)

    content=result.get("content","").lower()

    title=result.get("url","").lower()


    # Wikipedia ללא תוכן לא מתקבל
    if result.get("source")=="Wikipedia":

        if len(content)<50:
            return False


    # Wikidata חייב להכיל התאמה כלשהי
    if result.get("source")=="Wikidata":

        words=q.split()

        if not any(
            len(w)>2 and w in content
            for w in words
        ):
            return False


    return True



def validate_result(question,result):

    if not result:
        return False

    source=result.get("source","")


    if not semantic_match(question,result):
        return False


    if source in [
        "Wikipedia",
        "Wikidata"
    ]:
        return True


    content=result.get("content","")

    return len(content)>=10


'''

text=text[:start]+new+text[end:]

p.write_text(text,encoding="utf8")

print("SEMANTIC FILTER ADDED")
