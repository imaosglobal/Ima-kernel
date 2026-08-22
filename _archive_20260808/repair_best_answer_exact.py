from pathlib import Path

p=Path("learning/web_knowledge_collector.py")
text=p.read_text(encoding="utf8")

start=text.find("def best_answer(question):")

if start==-1:
    raise Exception("best_answer not found")

new=r'''def best_answer(question):

    results=collect_sources(question)

    if not results:
        return None


    def rank(r):

        source=r.get("source","")
        content=r.get("content","")

        score=0

        # עדיפות למקור עם טקסט מלא
        if source=="Wikipedia":
            score += 100

        if source=="Wikidata":
            score += 20

        if len(content)>500:
            score += 50
        elif len(content)>100:
            score += 20

        # תוצאה קצרה מדי חשודה
        if len(content)<50:
            score -= 40

        return score


    valid=[]

    for r in results:
        if validate_result(question,r):
            valid.append(r)


    if not valid:
        return None


    valid.sort(
        key=rank,
        reverse=True
    )


    return valid[0]
'''

# חותכים את הפונקציה הישנה עד סוף הקובץ
text=text[:start]+new+"\n"

p.write_text(text,encoding="utf8")

