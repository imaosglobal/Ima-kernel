import json
import sys
from pathlib import Path
from datetime import date,timedelta

DB=Path.home()/".ima/truth/truth_database.jsonl"

q=" ".join(sys.argv[1:]).lower()

today=str(date.today())

if "היום" in q or "today" in q:
    q=q.replace("היום","").strip()


events=[]

if DB.exists():

    for line in DB.read_text().splitlines():

        try:
            events.append(
                json.loads(line)
            )
        except:
            pass


matches=[]

for e in events:

    text=json.dumps(
        e,
        ensure_ascii=False
    ).lower()

    if not q:
        matches.append(e)

    elif any(
        word in text
        for word in q.split()
    ):
        matches.append(e)


print("IMA TRUTH V2")
print("================")

if not matches:
    print("אין מידע מתועד")
else:

    print(
        "נמצאו",
        len(matches),
        "אירועים"
    )

    for e in matches[-15:]:

        if "event" in e:
            print(
                f"[{e.get('date',e.get('time'))}] {e['event']}"
            )

        else:
            print(
                json.dumps(
                    e,
                    ensure_ascii=False
                )[:500]
            )
