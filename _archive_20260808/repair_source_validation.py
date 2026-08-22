from pathlib import Path

p=Path("learning/web_knowledge_collector.py")

text=p.read_text(encoding="utf8")


start=text.index("def validate_result")
end=text.index("def best_answer")


new=r'''
def normalize_term(x):

    return (
        x
        .replace("מה זה ","")
        .replace("מהי ","")
        .replace("?","")
        .strip()
        .lower()
    )


def validate_result(question,result):

    if not result:
        return False

    content=result.get("content","").strip()

    if len(content)<20:
        return False


    q=normalize_term(question)

    text=content.lower()


    # התאמה ישירה
    if q in text:
        return True


    # התאמה חלקית
    words=q.split()

    for word in words:

        if len(word)>=3 and word[:3] in text:
            return True


    # מקור חיצוני מוכר עם תוכן מספיק
    if result.get("source") in [
        "Wikipedia",
        "Wikidata"
    ]:
        return True


    return False


'''


text=text[:start]+new+text[end:]

p.write_text(text,encoding="utf8")

