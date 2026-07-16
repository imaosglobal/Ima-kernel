from pathlib import Path

p=Path("ima_question_engine.py")

text=p.read_text()

text=text.replace(
'''def answer(question):

    q=question.lower()

    words=q.split()
''',
'''def answer(question):

    q=question.lower()

    words=q.split()

    today="2026-07-16"
'''
)

text=text.replace(
'''    if any(x in q for x in ["היום","נוצר","עשינו","בוצע"]):

        print("אירועים אחרונים:")
        for e in search_truth(words+["IMA","system","evolution"]):
            print(json.dumps(e,ensure_ascii=False)[:500])
            print("---")
''',
'''    if any(x in q for x in ["היום","נוצר","עשינו","בוצע"]):

        print("מצב היום מתוך שכבות IMA:")

        system=load_json(SYSTEM)

        if system:
            print(json.dumps(system,ensure_ascii=False,indent=2))
            print("---")

        for file in EVOLUTION.glob("*.json"):

            data=load_json(file)

            if data:
                print(file.name)
                print(json.dumps(data,ensure_ascii=False)[:700])
                print("---")

        print("אירועי אמת נוספים:")

        for e in search_truth(words+["2026-07-16","IMA"]):
            print(json.dumps(e,ensure_ascii=False)[:500])
            print("---")
'''
)

p.write_text(text)

print("QUESTION ENGINE V2 READY")
