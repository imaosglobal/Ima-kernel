import json
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

        for e in search_truth(words+["IMA","system","evolution"]):
''',
'''    if any(x in q for x in ["היום","נוצר","עשינו","בוצע"]):


        system=load_json(SYSTEM)

        if system:

        for file in EVOLUTION.glob("*.json"):

            data=load_json(file)

            if data:


        for e in search_truth(words+["2026-07-16","IMA"]):
'''
)

p.write_text(text)

